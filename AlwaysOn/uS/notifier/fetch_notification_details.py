import httpx
from typing import Optional, Dict, Any,List
import logging

GATEWAY_URL = "http://127.0.0.1:8000/permanent/alarm_processing"  # URL del endpoint del gateway

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('notif_details') 


async def get_event_data(event_to_notify:int,client:httpx.AsyncClient)-> Optional[Dict[str,Any]]:
    try:
        event = await client.get(
            f"{GATEWAY_URL}/fetch_event_details/",
            params={"details_for": event_to_notify}
        )
        event.raise_for_status()
        event_data=event.json()

        if not event_data:
            logger.error('No event details returned')
            return None

        return event_data
        
    except Exception as system_e:
        logger.exception(f'Exception ocurred while obtaining the event details{system_e}')
        return None

async def get_notification_channel(meter_id:int,alarm_level:int,client:httpx.AsyncClient)->Optional[str]:
    return 'email'


async def get_recipients(meter_id:int,notif_channel:str,client:httpx.AsyncClient)->Optional[List[str]]:
    
    try:
        match notif_channel:
            case 'email':
                channel_path="/fetch_recipients_email/"
            case 'sms':
                channel_path="/fetch_recipients_number/"

        recipients=await client.get(
            f"{GATEWAY_URL}{channel_path}",
            params={"meter_id": meter_id}
        )

        recipients.raise_for_status()
        
        if not recipients:
            logger.error('No communication details returned')

        recipients_list=recipients.json()

        return recipients_list

    except Exception as e:
        logger.exception(f'Exception ocurred while obtaining the recipients {e}')
        return None

async def get_receiver_data(meter_id:int,client:httpx.AsyncClient)-> Optional[Dict[str,Any]]:

    nicknames=await client.get(
        f"{GATEWAY_URL}/fetch_nicknames/",
        params={"meter_id": meter_id}
    )
    nicknames.raise_for_status()
    nicknames_data=nicknames.json()

    if not nicknames_data:
        logger.error('No nicknames for meter and project returned')
        return None

    return{
        'project_nickname': nicknames_data['project_nickname'],
        'meter_nickname':nicknames_data['meter_nickname'],
    }

async def get_notification_data(event_id:int,client:httpx.AsyncClient)-> Optional[Dict[str,Any]]:
    event_data=await get_event_data(event_id,client)                  
    if not event_data:
        return None
    
    project_data=await get_receiver_data(event_data['meter_id'],client)
    if not project_data:
        return None
    
    notif_channel=await get_notification_channel(event_data['meter_id'],event_data['level'],client)
    if not notif_channel:
        return None
    
    notification_recipients=await get_recipients(event_data['meter_id'],notif_channel,client)
    if not notification_recipients:
        return None
        
    receiver_data={
        'project_name':project_data['project_nickname'],
        'meter_nickname':project_data['meter_nickname'],
        'channel':notif_channel,
        'recipients_list':notification_recipients
    }

    final_notif={
        'receiver_data':receiver_data,
        'event_data':event_data
    }
    
    return final_notif
