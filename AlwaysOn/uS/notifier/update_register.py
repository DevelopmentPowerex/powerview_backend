from typing import Optional, Any, Dict
import httpx

import logging

from .config import settings

from .protocols.endpoints import NEW_NOTIFICATION_REG , UPDATE_INCIDENTS , UPDATE_LAST_NOTIFICATION

logger = logging.getLogger(__name__)

async def new_reg_notification(event_id:int,event_counter:int,client:httpx.AsyncClient): #Registrar en la DB la notificación enviada

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
        logger.debug(f"Sent event {event_id} for registering the new event notification")
        return register_notification_sent.status_code == 200        
    
    except httpx.HTTPError as e:
        logger.error(f"Error sending to gateway: {str(e)}")
        return None


async def update_counters(notif_id:int,event_id:int,client:httpx.AsyncClient): 
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
        data = response.json()

        return data.get('new_count')

    
    except httpx.HTTPError as e:
        logger.error(f"Error sending to gateway: {str(e)}")
        return False
    
    
async def remind_event(notif_id:int,event_id:int,client:httpx.AsyncClient):
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
        
        return response.status_code == 200        

    except httpx.HTTPError as e:
        logger.error(f"Error sending to gateway: {str(e)}")
        return False

