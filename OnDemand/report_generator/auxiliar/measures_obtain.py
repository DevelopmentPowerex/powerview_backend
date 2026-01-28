import asyncio
from datetime import datetime

import httpx
from typing import Optional,Any,Dict,List

from statistics import mean

import logging
logger = logging.getLogger(__name__)

GATEWAY_URL = "http://127.0.0.1:8000/displayable"  # URL del endpoint del gateway interno

PARAMETERS_FILTER=[# Parametros que se deben eliminar de la extracción por falta de uso
    "Signal_strength", #Frecuencia e intensidad de señal de transmisión
    "P_Active_demand", ##Demanda de potencia activa positiva actual
    "ICCID", #identificador único de placa
    "PT", #Valor de transformador de potencia del medidor
    "CT", #Valor de transformador de corriente del medidor (relación de transformación)
    "R_Active_demand", #Demanda de potencia activa inversa actual
    "P_Reactive_demand", #Demanda de potencia reactiva positiva actual
    "R_Reactive_demand", #Demanda de potencia reactiva inversa actual
    "kWh_spike", #Energía total activa en "periodo spike"
    "kWh_peak", #Energía total activa en "periodo peak"
    "kWh_flat", #Energía total activa en "periodo flat"
    "kWh_valley", #Energía total activa en "periodo valley"
    "C1_kvarh", #Energía reactiva en 1er cuadrante
    "C2_kvarh", #Energía reactiva en 2do cuadrante
    "C3_kvarh", #Energía reactiva en 3er cuadrante
    "C4_kvarh"  #Energía reactiva en 4to cuadrante 
] 

async def extract_measures(meter_id:int,start_date:datetime,end_date:datetime,client:httpx.AsyncClient):
    try:
        response = await client.get(
            f"{GATEWAY_URL}/extract_measures/",
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
    
    except Exception as e:
        logger.error(f"Something went wrong while asking for the measure register: {e}")

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
                logger.error('No measures returned')    
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

        except Exception as e:
            logger.error(f'Unexpected error in main process: {e}')

if __name__ == "__main__":  

    try:
        asyncio.run(extract_all(1,"2025-08-25T09:10:00","2025-08-25T13:00:00")) #qué medidor en qué rango
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt: Shutting down service")

