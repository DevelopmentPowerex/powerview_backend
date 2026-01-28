import asyncio
from datetime import datetime

import httpx
from typing import Optional,Any,Dict

import logging
logger = logging.getLogger(__name__)

PROJECT_ORDER="Proyecto_base"

async def obtain_project_info(project_name:str)->Optional[Dict[str,Any]]:
    #nombre del cliente, nombre del proyecto, cvs(abreviación) y fae (id)
    
    project_info={
        "id":1,
        "client_name": "ELECTROPROTECCIONES SAS",
        "project_name": "Alimentación Taller Dept.Técnico",
        "fae_id": 1,
        "csv_part1":"electro"
    }
    return project_info

async def obtain_meters(project_id:int)->Optional[Dict[str,Any]]:
    #Recibo el nombre del proyecto, retorno una lista de los medidores que tiene y cómo se llama su circuito
    meters_list= {
        "models":["PV-M3"],
        "circuits": {
            "1":"Tablero Alimentación"
        }
    }
    return meters_list

async def obtain_fae_info(fae_id:int)->Optional[Dict[str,Any]]:
    fae_info= {
        "company_name":"PREMIUMENERGIA SAS",
        "engineer_name":"Ing. Jeramhil Javier Solis Yari",
        "email_addr":"proyectos@premium-energia.com",
        "phone":"0984373697"
    }
    return fae_info

async def project_data_extraction(searched_project:str)->Optional[Dict[str,Any]]: #MAIN

    project_info= await obtain_project_info(searched_project)

    if not project_info:
        logger.error('No information available for the specified project')
        return None
    
    meters_list = await obtain_meters(project_info['id'])

    if not meters_list:
        logger.error('No meters returned for the specified project')
        return None
    
    if project_info['fae_id']:
        fae_info = await obtain_fae_info(project_info['fae_id'])

        if not fae_info:
            logger.error('FAE info for this project is missing')
            return None

    project_details={

        'client_name':project_info['client_name'],
        'project_name':project_info['project_name'],
        'fae':fae_info,
        'meters_models': meters_list['models'],
        'circuits': meters_list['circuits'],
        'csv_1st':project_info["csv_part1"]

    }

    #logger.info(project_details)

    return project_details

  
if __name__ == "__main__":  
    success = asyncio.run(project_data_extraction(PROJECT_ORDER))

    if success:
        logger.info('tamo gussi') 
    else:
        logger.error('mal mal mal') 