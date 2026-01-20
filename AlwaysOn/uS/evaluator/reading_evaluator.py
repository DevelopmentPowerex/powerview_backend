#uS dedicado a evaluar las reglas de alarmas por cada escritura en la DB
from AlwaysOn.rabbit.rabbit_func import read_id

from typing import Dict, Any, Optional
import asyncio
import httpx

from .protocols.operators_list import operators
from .protocols.endpoints import SAVE_NEW_EVENT_ENDPOINT, GET_RULES_ENDPOINT

from dotenv import load_dotenv
load_dotenv("./AlwaysOn/uS/evaluator/.env.local")

from .config import settings
from .shared.logging_config import setup_logging

setup_logging(settings.log_level)

import logging
logger = logging.getLogger(__name__)

async def obtain_id()-> Optional[int]:#Obtener id de le medición a evaluar
    #Leer el último id publicado en el queue para alarmas de rabbit
    try:
        recent_measure_id=await read_id(settings.rabbit_thread,settings.rabbit_url) #Llamar a la función externa para obtener el id
        just_id=recent_measure_id[0][recent_measure_id[1]]
        return just_id
    except Exception as e:
        logger.error(f'Error reading the id for the latest measurement {e}')
        return None

async def obtain_rules(received_id:int,client: httpx.AsyncClient)->Optional[dict[str,Any]]: #Con id obtenido, traemos las reglas

    try:
        logger.debug(f'Evaluate reading id: {received_id}')      
        
        response = await client.get(
            f"{settings.gateway_url}{GET_RULES_ENDPOINT}",
            params={"measure_id": received_id}
        )

        response.raise_for_status()
        response_data=response.json()

        if not response_data:
            logger.debug(f'No rules for: {received_id}')    
            return None

        rules=response_data.get('rules',None)
        if not rules:
            logger.warning(f'Reading {received_id} returned no rules')      
            return None
        
        parameters=response_data.get('param_values',None)
        if not parameters:
            logger.warning(f'Reading {received_id} returned no parameters')     
        
        logger.debug(f'Reading {received_id} has to be evaluated under {len(rules)} rules')      

        return {
            'measure_id':received_id,
            'rules': rules,
            'parameters': parameters
        }
            
    except httpx.HTTPError as e:
        logger.error(f'Error sending to gateway {str(e)}')
        return None

async def rule_evaluator(data_for_ev:dict[str,Any])->Optional[Dict[str,Any]]: #Las reglas extraídas hay que evaluarlas
    
    measure_id=data_for_ev['measure_id'] #id de la medición 
    rules=data_for_ev['rules'] #contiene las reglas encontradas, aplicables para la medición
    parameters=data_for_ev['parameters'] #Contiene los valores leidos de la medición
    
    broken_rules_id=[]
    #logger.debug(rules)
    try: 
        for rule in rules:
            
            param_name = rule['parameter']
            comparator = rule['comparator']
            threshold = rule['threshold']
            id=rule['id']

            current_value = parameters.get(param_name)
            if current_value is None:
                logger.warning(f"Missing parameter '{param_name}' for rule {id} (measure {measure_id})")
                continue

            compare_func = operators.get(comparator)    
            
            if compare_func is None:
                logger.warning(f"Unknown comparator '{comparator}' in rule {id}")
                continue

            if compare_func(current_value, threshold):
                logger.debug(f'Rule {id} BROKEN')
                broken_rules_id.append(id)

            else: 
                logger.debug(f'Rule {id} OK')
    
        if broken_rules_id:
            logger.debug(f'Broken rules for id {measure_id}: {broken_rules_id}')
            
            return {
                'measure_id':measure_id,
                'broken_rules': broken_rules_id,
            }
        
        else:
            logger.debug(f'No broken rules for {measure_id}')
            return None
        
    except Exception as e:
        logger.error(f'Error checking the rules {e}')
        return None
   
async def send_events(broken_rules:Dict[str,Any],client: httpx.AsyncClient):
    try:
        #Envío al gateway interno para que registre los eventos en la DB
        response = await client.post(
                    f"{settings.gateway_url}{SAVE_NEW_EVENT_ENDPOINT}",
                    json=broken_rules
                )
        
        response.raise_for_status()
        event=response.json()
        logger.info(f"measurement: {broken_rules['measure_id']} | broken: {broken_rules['broken_rules']} | reg: {event[0]['id']}")
        return
    except httpx.HTTPError as e:
        logger.error(f"Error sending to gateway: {str(e)}")
        return
    
async def main():
    logger.info('Initializing Measurement evaluator')
    async with httpx.AsyncClient(timeout=settings.gateway_timeout) as client:
        while True:
            try:
                measurement_id = await obtain_id() 
                if measurement_id is None:
                    continue

                rules_per_id=await obtain_rules(measurement_id,client)

                if not rules_per_id:
                    continue

                ev_results=await rule_evaluator(rules_per_id)

                if ev_results:
                    await send_events(ev_results,client)
                                
            except Exception as e:
                logger.error(f'Unexpected error in main process: {e}')

if __name__=="__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt: Shutting down service")

