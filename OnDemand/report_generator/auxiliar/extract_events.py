import asyncio
import json
from datetime import datetime
import httpx
from typing import Optional,Any,Dict,List

import logging
logger = logging.getLogger(__name__)

GATEWAY_URL = "http://127.0.0.1:8000/displayable"  # URL del endpoint del gateway interno

M3_MAPPING={ # Mapeo de constantes de mensaje PV-M3
    0:"serial_number",
    1: "vA", 2: "vB", 3: "vC", #Voltajes de cada línea
    4: "vAB", 5: "vBC", 6: "vCA", #Voltajes de cada fase
    7: "iA", 8: "iB", 9: "iC", #Corrientes de cada línea
    10: "PA", 11: "PB", 12: "PC", 13: "P", #Potencia Activa por línea y total
    14: "QA", 15: "QB", 16: "QC", 17: "Q", #Potencia Reactiva por línea y total
    18: "SA", 19: "SB", 20: "SC", 21: "S" , #Potencia Aparente por línea y total
    22: "PFA",23: "PFB",24: "PFC",25: "PF", #Factor de Potencia por línea y total
    26: "F", 27:"Signal_strength", #Frecuencia e intensidad de señal de transmisión
    28: "P_kWh_T", #Indication value of total positive active energy
    29: "R_kWh_T", #Indication value of total reverse active energy
    30: "P_kvarh_T", #Indication value of total positive reactive energy
    31: "R_kvarh_T", #Indication value of total reverse reactive energy
    32: "P_Active_demand", ##Demanda de potencia activa positiva actual
    33: "ICCID", #identificador único de placa
    34: "PT", #Valor de transformador de potencia del medidor
    35: "CT", #Valor de transformador de corriente del medidor (relación de transformación)
    36: "TA", 37: "TB", 38: "TC", 39: "TN", #Temperaturas en líneas y neutro
    40: "iF", #Corriente de fuga
    41: "DI_status", #Estado de las entradas digitales (bit0:DI1,bit1:DI2,bit2:DI3,bit3:DI4)
    42: "P_kWh_A", 43: "R_kWh_A", #Energía activa en A: Positiva e Inversa/Reversa
    44: "P_kvarh_A", 45: "R_kvarh_A", #Energía reactiva en A: Positiva e Inversa/Reversa
    46: "P_kWh_B", 47: "R_kWh_B", #Energía activa en B: Positiva e Inversa/Reversa
    48: "P_kvarh_B", 49: "R_kvarh_B", #Energía reactiva en B: Positiva e Inversa/Reversa
    50: "P_kWh_C", 51: "R_kWh_C", #Energía activa en C: Positiva e Inversa/Reversa
    52: "P_kvarh_C", 53: "R_kvarh_C", #Energía reactiva en C: Positiva e Inversa/Reversa
    54: "THD_A", 55: "THD_B", 56: "THD_C" , #Rate de harmonicos de voltaje por línea
    57: "THDC_A",58: "THDC_B",59: "THDC_C", #Rate de harmonicos de corriente por línea
    60: "R_Active_demand", #Demanda de potencia activa inversa actual
    61: "P_Reactive_demand", #Demanda de potencia reactiva positiva actual
    62: "R_Reactive_demand", #Demanda de potencia reactiva inversa actual
    63: "V_unb", #Desbalance de voltaje en %
    64: "I_unb", #Desbalance de corriente en %
    65: "kWh_spike", #Energía total activa en "periodo spike"
    66: "kWh_peak", #Energía total activa en "periodo peak"
    67: "kWh_flat", #Energía total activa en "periodo flat"
    68: "kWh_valley", #Energía total activa en "periodo valley"
    69: "C1_kvarh", #Energía reactiva en 1er cuadrante
    70: "C2_kvarh", #Energía reactiva en 2do cuadrante
    71: "C3_kvarh", #Energía reactiva en 3er cuadrante
    72: "C4_kvarh"  #Energía reactiva en 4to cuadrante 
}

async def get_events_from_DB(extract_ids:List,start_date:str,end_date:str,client:httpx.AsyncClient):
   
    response = await client.get(
            f"{GATEWAY_URL}/extract_events/",
            params={"meter_list":extract_ids,
                    "start_date":start_date,
                    "end_date":end_date
                    }
        )

    response.raise_for_status()
    response_data=response.json()
    
    if not response_data:
        logger.info(f'No events returned for meters: {extract_ids}')    
        return None
    
    return response_data

async def get_triggers_datetimes(first_trigger:int,last_trigger:int,client:httpx.AsyncClient):
    response = await client.get(
            f"{GATEWAY_URL}/extract_triggers_ts/",
            params={"first_trigger":first_trigger,
                    "last_trigger":last_trigger}
        )
    
    response.raise_for_status()
    response_data=response.json()

    if not response_data:
        logger.info(f'Couldnt find a proper timestamp')    
        return None
        
    return response_data if len(response_data)>1 else [response_data[0],response_data[0]]

async def format_rule(rule:Dict[str,Any]):
    
    new_rule=M3_MAPPING[rule['parameter']]+rule['comparator']+str(rule['threshold'])
    
    match rule['level']:
        case 1:
            new_level="Alta"
        case 2:
            new_level="Media"
        case 3:
            new_level="Baja"
        case _:
            new_level="Baja"

    return new_rule,new_level

async def get_rule_details(rule_id:int,client:httpx.AsyncClient):
    response = await client.get(
            f"{GATEWAY_URL}/extract_rule_info/",
            params={"rule_id":rule_id}
        )
    
    response.raise_for_status()
    response_data=response.json()
    
    if not response_data:
        logger.info(f'No details returned for rule: {rule_id}')    
        return None

    formated_rule,event_level=await format_rule(response_data)

    return formated_rule,event_level

async def get_circuit_name(rule_id:int,client:httpx.AsyncClient):
    response = await client.get(
            f"{GATEWAY_URL}/extract_circuit_name/",
            params={"rule_id":rule_id}
        )
    
    response.raise_for_status()
    response_data=response.json()
    
    if not response_data:
        logger.info(f'No circuit name returned for rule: {rule_id}')    
        return None

    return response_data

async def get_events_details(events_list,client:httpx.AsyncClient):
    new_event_list=[]

    for event in events_list:
        triggers_ts= await get_triggers_datetimes(event['first_trigger'],event['last_trigger'],client)
        
        rule_info,event_level=await get_rule_details(event['rule_id'],client)

        circuit_name=await get_circuit_name(event['rule_id'],client)

        new_event_list.append({
            "circuit":circuit_name.replace('_',' '),
            "broken_rule":rule_info,
            "first_event":(triggers_ts[0]).replace('T',' '),
            "last_event":(triggers_ts[1]).replace('T',' '),
            "event_counter":event['event_counter'],
            "alarm_level": event_level
        }
        )    

    return new_event_list, events_list

async def extract_order(extract_ids:List,start_date:str,end_date:str):
    async with httpx.AsyncClient() as client:
        events_DB:list=await get_events_from_DB(extract_ids,start_date,end_date,client)
        if not events_DB:
            logger.error('The extracting function returned None')
        
        new_events_list,og_event_list=await get_events_details(events_DB,client)


        return new_events_list,og_event_list




