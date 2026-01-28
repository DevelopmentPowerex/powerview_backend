import httpx
from typing import Dict,List

from ..config import settings
from ..protocols.auxiliar_info import PREMADE_ORDERS

import logging
logger = logging.getLogger(__name__)

async def rule_details(rule_id:int,client:httpx.AsyncClient):
    
    response = await client.get(
            f"{settings.gateway_url}/extract_rule_info/",
            params={"rule_id":rule_id}
        )
    
    response.raise_for_status()
    response_data=response.json()
    
    if not response_data:
        logger.warning(f'No details returned for rule: {rule_id}')    
        return None

async def get_time_limits(event_low_limit:int,event_upper_limit:int,client:httpx.AsyncClient):
    response = await client.get(
            f"{settings.gateway_url}/extract_event_time_limits/",
            params={"lower_limit":int,
                    "upper_limit":int}
        )
    
    response.raise_for_status()
    response_data=response.json()
    
    if not response_data:
        logger.info(f'The timestamps for the required ids were not obtained')    
        return None

    return response_data['lower_limit'],response_data['upper_limit']

async def events_graphs_order(event_list:List[Dict[str,int]]):
    
    event_full_list=[]
    for event in event_list:
        rule_translation=await rule_details(event['rule_id'])
        event_parameter=rule_translation['parameter']

        for order_code,order_content in PREMADE_ORDERS.items():
            if event_parameter in [PREMADE_ORDERS[order_code]][0]:
                parameter_family=order_code
        
        lower_timestamp,upper_timestamp = await get_time_limits(event['first_trigger'],event['last_trigger'])

        event_full_list.append({
            **event,
            'parameter_name': event_parameter,
            'parameter_family': parameter_family,
            'graph_start': lower_timestamp,
            'graph_end': upper_timestamp
        })

    #Aqui debo tener la misma cantidad de cosas, pero con el nombre y ts correspondientes
    logger.debug(event_full_list)

    events_per_family={}
    for event in event_full_list:
        if event['parameter_family'] not in events_per_family.keys():
            events_per_family.update((event['parameter_family'],[]))

        events_per_family[event['parameter_family']].append(event)

    #Aqui debo tener un diccionario cuyas llaves son las familias, y los valores de esas llaves son cada evento que le pertenece
    logger.debug(events_per_family)



    



