#uS dedicado a evaluar las reglas de alarmas por cada escritura en la DB
from AlwaysOn.rabbit.rabbit_func import read_id

import logging
from typing import Dict, Any, Optional
import asyncio
import httpx

import operator

GATEWAY_URL = "http://127.0.0.1:8000/permanent/rule_evaluator"  # URL del endpoint del gateway interno

operators={
    '<' : operator.lt,
    '<=' : operator.le,
    '>' : operator.gt,
    '>=' : operator.ge,
    '=' : operator.eq,
    '!=' : operator.ne
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('evaluator') #Logger específico para Evaluador de Alarmas

async def obtain_id()-> Optional[int]:#Obtener id de le medición a evaluar
    #Leer el último id publicado en el queue para alarmas de rabbit
    try:
        recent_measure_id=await read_id('EV_RECV') #Llamar a la función externa para obtener el id
        just_id=recent_measure_id[0][recent_measure_id[1]]
        return just_id
    except Exception as e:
        logger.error(f'Error reading the id for the latest measurement {e}')
        return None

async def obtain_rules(received_id:int,client: httpx.AsyncClient)->Optional[dict[str,Any]]: #Con id obtenido, traemos las reglas

    try:
        logger.info(f'Sent id {received_id} for extracting the rules')      
        
        response = await client.get(
            f"{GATEWAY_URL}/get_rules/",
            params={"request": received_id}
        )

        response.raise_for_status()
        response_data=response.json()

        if not response_data:
            logger.info(f'No rules returned for Measure id: {received_id}')    
            return None

        rules=response_data['rules']
        parameters=response_data['param_values']

        logger.info(f'Measure id: {received_id} returned {len(rules)} rules')      
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

    try: 
        for rule in rules:
            
            param_name = rule['parameter']
            comparator = rule['comparator']
            threshold = rule['threshold']
            id=rule['id']
            current_value = parameters.get(param_name)
            compare_func = operators.get(comparator)

            if compare_func(current_value, threshold):
                logger.info(f'Rule {id} BROKEN')
                broken_rules_id.append(id)

            else: 
                logger.info(f'Rule {id} OK')
    
        if broken_rules_id:
            logger.info(f'Broken rules for id {measure_id}: {broken_rules_id}')
            return {
                'measure_id':measure_id,
                'broken_rules': broken_rules_id,
            }
        
        else:
            logger.info(f'No broken rules for {measure_id}')
            return None
        
    except Exception as e:
        logger.error(f'Error checking the rules {e}')
        return None
   
async def send_events(broken_rules:Dict[str,Any],client: httpx.AsyncClient):
    try:
        #Envío al gateway interno para que registre los eventos en la DB
        response = await client.post(
                    f"{GATEWAY_URL}/save_new_event/",
                    json=broken_rules
                )
        
        response.raise_for_status()
        logger.info(f"Sent events: Broken rules {broken_rules['broken_rules']} on measure {broken_rules['measure_id']}")
        
    except httpx.HTTPError as e:
        logger.error(f"Error sending to gateway: {str(e)}")

async def shutdown():
    logger.info("Shutting down...ALM_EV uS")
    # 1. Cancelar todas las tareas pendientes excepto la actual
    pending = asyncio.all_tasks()
    current_task = asyncio.current_task()
    
    pending_tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in pending_tasks:
        task.cancel()
    
    try:
        await asyncio.gather(*pending_tasks, return_exceptions=True)
    except Exception as e:
        logger.warning(f"Failed cancelling some tasks: {e}")


    # 4. Cerrar cliente HTTP (si existe)
    if 'http_client' in globals() and http_client:
        await http_client.aclose()
        logger.info("Cliente HTTP cerrado")
    
    logger.info("Shut down completed")

async def main():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                measurement_id = await obtain_id() 
                
                if measurement_id:
                    rules_per_id=await obtain_rules(measurement_id,client)

                    if rules_per_id:
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

