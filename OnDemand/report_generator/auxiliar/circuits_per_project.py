import asyncio

import httpx
from typing import Optional,Any,Dict, List

import logging
logger = logging.getLogger(__name__)


async def get_project_circuits(client_name:str,searched_project:str)->Optional[List[Dict[str,Any]]]: 

    #Aquí se debe consultar por http al gateway para que retorne lo que queremos
    #Buscamos tener los circuitos pertenecientes

    circuits_info=[
        {
            'meter_id':1,
            'circuit_name':"nombre ejemplo 1",
            'meter_model': 'modelo ejemplo 1',
            'sn':"1234567890"
        },
        {
            'meter_id':2,
            'circuit_name':"nombre ejemplo 2",
            'meter_model': 'modelo ejemplo 2',
            'sn':"1987654321"
        }
    ]

    logger.debug(circuits_info)

    return circuits_info

  
if __name__ == "__main__":  
    success = asyncio.run(get_project_circuits())
