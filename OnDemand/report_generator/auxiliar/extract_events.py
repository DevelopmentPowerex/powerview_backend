import httpx
from typing import List, Optional,Dict,Any

from ..config import settings
from ..protocols.endpoints import EXTRACT_EVENTS_ENDPOINT

import logging
logger = logging.getLogger(__name__)

async def fetch_events(extract_ids:List,start_date:str,end_date:str,client:httpx.AsyncClient)->Optional[List[Dict[str,Any]]]:
    try:
        response = await client.get(
                f"{settings.gateway_url}{EXTRACT_EVENTS_ENDPOINT}",
                params={"meter_list":extract_ids,
                        "start_date":start_date,
                        "end_date":end_date
                        }
            )

        response.raise_for_status()
        response_data=response.json()

        if not response_data:
            logger.error(f'No events returned for meters: {extract_ids}')    
            return None
        return response_data
    
    except Exception:
        logger.exception(f"Error fetching events for meters {extract_ids}")
        return None






