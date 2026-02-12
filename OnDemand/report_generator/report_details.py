import asyncio
import httpx
from typing import Optional, Dict, Any

from OnDemand.report_generator.auxiliar.circuits_per_project import get_project_circuits
from OnDemand.report_generator.auxiliar.measures_obtain import fetch_readings as extract_readings
from OnDemand.report_generator.auxiliar.extract_events import fetch_events as extract_events

from .config import settings

import logging
logger = logging.getLogger(__name__)
    
async def fetch_report_data(client_name:str,project_name:str,start_date:str,end_date:str)->Optional[Dict[str,Any]]:
    
    async with httpx.AsyncClient(timeout=settings.gateway_timeout) as client:
        
        circuits=await get_project_circuits(client_name,project_name ,client) 
        logger.debug(circuits)
        if not circuits:
            logger.error(f'Error fetching the meters of {project_name}')
            return None

        meter_list=[]
        for circuit_key in circuits:
            meter_list.append(circuit_key['id'])
        logger.debug(meter_list)

        measurements, extreme_values=await extract_readings(meter_list,start_date,end_date,client) 
        logger.debug(extreme_values)
        if not (measurements):
            logger.error('Error while getting the readings information')
            return None

        event_list=await extract_events(meter_list,start_date,end_date,client) 
        logger.debug(event_list)
        if not event_list:
            logger.error('Error while obtaining the events/alarms register')
        
        return {
            'circuits':circuits,
            'report':extreme_values,
            'events':event_list,
            'readings':measurements
        }
        

async def main():
    test_report=await fetch_report_data('ELECTROPROTECCIONES SAS','Proyecto A',"2026-01-27T17:48:00","2025-10-28T22:00:00")

if __name__=="__main__":

    asyncio.run(main())
