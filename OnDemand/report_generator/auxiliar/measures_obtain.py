import asyncio
from datetime import datetime

import httpx
from typing import Optional,Any,Dict,List

from statistics import mean

from ..config import settings
from ..protocols.auxiliar_info import PARAMETERS_FILTER

import logging
logger = logging.getLogger(__name__)

async def extract_measures(meter_id:int,start_date:datetime,end_date:datetime,client:httpx.AsyncClient):
    try:
        response = await client.get(
            f"{settings.gateway_url}/extract_measures/",
            params={"meter_id":meter_id,
                    "start_date":start_date,
                    "end_date":end_date,
                    }
        )

        response.raise_for_status()
        response_data=response.json()

        if not response_data:
            logger.info(f'No measures returned for meter: {meter_id}')    
            return None

        return response_data
    
    except Exception:
        logger.exception(f"Something went wrong while asking for the measure register")

async def data_filter(unfiltered:List)->Optional[List[Dict[str,Any]]]:
    
    for measure in unfiltered:
        measure.pop('id',None)
        for unwanted_param in PARAMETERS_FILTER:
            measure['parameters'].pop(unwanted_param,None)

    filtered_data=unfiltered

    return filtered_data

async def calculate_extreme(measurement_list:List[Dict[str,Any]])->Optional[Dict[str,Any]]:

    timestamps = [m["timestamp"] for m in measurement_list]
    start_time = min(timestamps)
    end_time = max(timestamps)

    parameters_by_key: Dict[str, List[float]] = {}

    for measure in measurement_list:
        for param_key, param_val in measure["parameters"].items():
            parameters_by_key.setdefault(param_key, []).append(param_val)  #diconario de "key":[todos los valores leidos]

    extremes: Dict[str, Dict[str, float]] = {}
    for param_name, read_values in parameters_by_key.items():
        extremes[param_name] = {
            "max": max(read_values),
            "min": min(read_values),
            "prom": round(mean(read_values), 2)
        }

    extreme_values={
        'meter_id':measurement_list[0]['meter_id'],
        'start_time':start_time,
        'end_time':end_time,
        'extreme_values':extremes
    }

    return extreme_values

async def extract_all(meter_id:int,start_date:datetime,end_date:datetime):

    async with httpx.AsyncClient() as client:
        try:
            extracted_measurements = await extract_measures(meter_id,start_date,end_date,client) 
            
            if not extracted_measurements:
                logger.error(f'No measures returned for meter {meter_id}')    
                return None
            
            filtered_measurements=await data_filter(extracted_measurements)
            if not filtered_measurements:
                logger.error('Couldnt filter the measurements')
                return None

            #logger.info(filtered_measurements)

            extreme_values=await calculate_extreme(filtered_measurements)
            if not extreme_values:
                logger.error('Couldnt determine the extreme values on this period of time')
                return None
            
            return filtered_measurements,extreme_values   #retornar los valores extremos dentro del rango y las mediciones completas

        except Exception:
            logger.exception(f'Unexpected error in main process')

if __name__ == "__main__":  

    try:
        asyncio.run(extract_all(1,"2025-08-25T09:10:00","2025-08-25T13:00:00")) #qué medidor en qué rango
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt: Shutting down service")

