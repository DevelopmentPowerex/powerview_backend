import httpx
from typing import Optional, Dict, Any

import logging
from .config import settings

from .protocols.endpoints import CHECK_NOTIFICATION_REGISTER

logger = logging.getLogger(__name__)

async def check_register(event_id:int,client:httpx.AsyncClient)-> Optional[tuple[str,int]]: 
    #Revisa si el id (la última alarma registrada en rabbit) ya fue guardado en tabla de notificaciones
    #Siempre que retorne None, significa que hay que realizar un registro nuevo, ya sea porque no se ha notificado o porque debe tomarse el evento como uno nuevo

    try:
             
        notification_register = await client.get(
            f"{settings.gateway_url}{CHECK_NOTIFICATION_REGISTER}",
            params={"event_id": event_id}
        )

        notification_register.raise_for_status()
        response_notification_register=notification_register.json()
        
        if not notification_register: 
            logger.info(f'This event has not been notified before')
            return None
                
        return response_notification_register
        
    except httpx.HTTPError as e:
        logger.error(f'Error asking to internal gateway {str(e)}')
        return None

        