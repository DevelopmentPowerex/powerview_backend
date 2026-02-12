import asyncio

import httpx
from typing import Optional,Any,Dict, List

from ..config import settings
from ..protocols.endpoints import FETCH_CIRCUITS_ENDPOINT

import logging
logger = logging.getLogger(__name__)

async def get_project_circuits(client_name:str,searched_project:str,client:httpx.AsyncClient)->Optional[List[Dict[str,Any]]]: 
    
    response = await client.get(
        f"{settings.gateway_url}{FETCH_CIRCUITS_ENDPOINT}",
        params={"client_name": client_name,
                "project_name":searched_project}
    )

    response.raise_for_status()
    response_data=response.json()

    if not response_data:
        logger.debug(f'No circuits for: {searched_project}')    
        return None
    
    return response_data

  
if __name__ == "__main__":  
    success = asyncio.run(get_project_circuits())
