import asyncio
from datetime import datetime

import httpx
from typing import Optional,Any,Dict,List

from statistics import mean

from ..config import settings
from ..protocols.auxiliar_info import PARAMETERS_FILTER, PREMADE_ORDERS
from ..protocols.endpoints import EXTRACT_MEASURES_ENDPOINT
import logging
logger = logging.getLogger(__name__)

async def extract_measures(meter_id:List,start_date:datetime,end_date:datetime,client:httpx.AsyncClient):
    try:
        response = await client.get(
            f"{settings.gateway_url}{EXTRACT_MEASURES_ENDPOINT}",
            params={"meters_ids":meter_id,
                    "start_date":start_date,
                    "end_date":end_date,
                    }
        )

        response.raise_for_status()
        response_data=response.json()

        if not response_data:
            logger.error(f'No measures returned for meter: {meter_id}')    
            return None

        return response_data
    
    except Exception:
        logger.exception(f"Something went wrong while asking for the measure register")

async def translate_values(extreme_values:Dict[str,Any]): 
    formatted_extremes={}
    report_extremes=[]
    for circuit in extreme_values:
        for report_parameter in PREMADE_ORDERS.keys():
            new_param_values=[]
            for parameter in PREMADE_ORDERS[report_parameter][0]:
                if not(circuit['extreme_values'][parameter]['max'] == 0 and circuit['extreme_values'][parameter]['min'] ==0 and circuit['extreme_values'][parameter]['prom'] == 0):
                    item={
                        'name':parameter,
                        'max':circuit['extreme_values'][parameter]['max'],
                        'min':circuit['extreme_values'][parameter]['min'],
                        'prom':circuit['extreme_values'][parameter]['prom']
                    }
                    
                    new_param_values.append(item)
            
            if new_param_values:
                formatted_extremes.update({
                    report_parameter:new_param_values
                })
            
        report_extremes.append({
            'meter_id':circuit['meter'],
            'start_time':circuit['start'],
            'end_time':circuit['end'],
            'extreme_values':formatted_extremes,
        })
    return report_extremes

async def calculate_extreme(meter_list:List[int],measurement_list:List[Dict[str,Any]])->Optional[Dict[str,Any]]:

    final_extremes=[]
    for meter in meter_list:
        timestamps=[]
        
        parameters_by_key: Dict[str, List[float]] = {}

        for reading in measurement_list:
            if reading['id']==meter:
                timestamps.append(reading['timestamp'])
                

                for param_key, param_val in reading["reading"].items():
                    parameters_by_key.setdefault(param_key, []).append(param_val)  #diconario de "key":[todos los valores leidos]
        
        
        extremes: Dict[str,     Dict[str, float]] = {}
        for param_name, read_values in parameters_by_key.items():
            extremes[param_name] = {
                "max": max(read_values),
                "min": min(read_values),
                "prom": round(mean(read_values), 2)
            }

        start_time = min(timestamps)
        end_time = max(timestamps)

        final_extremes.append({
            'meter':meter,
            'start':start_time,           
            'end':end_time,
            'extreme_values':extremes
            })
        
    logger.debug(final_extremes)

    report_extremes=await translate_values(final_extremes) #FORMATEAR VALORES EXTREMOS PARA SU USO
    logger.debug(report_extremes)
    if not report_extremes:
        logger.error('Error formatting the extreme values')
        
    return report_extremes

async def fetch_readings(meter_list:List,start_date:datetime,end_date:datetime,client:httpx.AsyncClient):

    try:
        extracted_measurements = await extract_measures(meter_list,start_date,end_date,client) 
        
        if not extracted_measurements:
            logger.error(f'No measures returned for meters {meter_list}')    
            return None,None
        
        report_values=await calculate_extreme(meter_list,extracted_measurements)
        if not report_values:
            logger.error('Couldnt determine the extreme values on this period of time')
            return None,None
        
        return extracted_measurements, report_values  #retornar los valores extremos dentro del rango y las mediciones completas
        
    except Exception:
        logger.exception(f'Unexpected error in main process')


