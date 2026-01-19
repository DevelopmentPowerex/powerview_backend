from typing import Optional, Any, Dict
import httpx

import logging

from .config import settings

from .protocols.endpoints import NEW_NOTIFICATION_REG , UPDATE_INCIDENTS , UPDATE_LAST_NOTIFICATION

logger = logging.getLogger(__name__)

async def new_reg_notification(event_id:int,event_counter:int,client:httpx.AsyncClient)->bool: #Registrar en la DB la notificación enviada

    new_register={
        'event_id':event_id,
        'event_counter':event_counter
    }

    try:
        register_notification_sent = await client.post(
                    f"{settings.gateway_url}{NEW_NOTIFICATION_REG}",
                    json=new_register
                )
        
        register_notification_sent.raise_for_status()

        logger.debug(f"{event_id} new event notification registered")
        return True
        
    except httpx.HTTPError as e:
        logger.error(f"Error sending to gateway: {e}")
        return False


async def update_counters(notif_id:int,event_id:int,client:httpx.AsyncClient)->Optional[int]: 
    #Cambiar el número contador en la tabla alarm_notif a +1 y ultimo trigger a este id
    
    update_info={
        'notif_id':notif_id,
        'event_id':event_id
    }

    try:
        logger.debug(f"Updating Notification {notif_id} counter and trigger")
        response = await client.post(
                    f"{settings.gateway_url}{UPDATE_INCIDENTS}",
                    json=update_info
                )
        
        response.raise_for_status()
        
        if not response.content:
            return None
        
        data = response.json()

        if not data:
            return None
        
        return data.get('new_count') 

    
    except httpx.HTTPError as e:
        logger.error(f"Error sending to gateway: {e}")
        return None
    
    
async def remind_event(notif_id:int,event_id:int,client:httpx.AsyncClient)->bool:
    #Si se logró enviar la notificación, actualizar el registro de notificaciones enviadas
    update_notif={
        'event_id':event_id,
        'notif_id':notif_id
    }

    try:
        logger.debug(f"Updating Notification register {event_id} as the last succesfully notified")
        response = await client.post(
                    f"{settings.gateway_url}{UPDATE_LAST_NOTIFICATION}",
                    json=update_notif
                )
        
        response.raise_for_status()

        logger.debug(f"Sent event {event_id} for registering the new event notification")
        return True
    
    except httpx.HTTPError as e:
        logger.error(f"Error sending to gateway: {e}")
        return False

