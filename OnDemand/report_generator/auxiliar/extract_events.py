import asyncio
import json
from datetime import datetime
import httpx
from typing import Optional,Any,Dict,List

from ..config import settings
from ..protocols.auxiliar_info import M3_MAPPING

import logging
logger = logging.getLogger(__name__)

async def get_events_from_DB(extract_ids:List,start_date:str,end_date:str,client:httpx.AsyncClient):
   
    response = await client.get(
            f"{settings.gateway_url}/extract_events/",
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
            f"{settings.gateway_url}/extract_triggers_ts/",
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
            f"{settings.gateway_url}/extract_rule_info/",
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
            f"{settings.gateway_url}/extract_circuit_name/",
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




