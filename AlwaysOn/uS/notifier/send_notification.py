import asyncio

from typing import Dict, Any, Optional
import httpx

from AlwaysOn.uS.notifier.fetch_notification_details import get_notification_data
from AlwaysOn.uS.notifier.email.send_email import notify_by_email

from dotenv import load_dotenv
load_dotenv(".env.local")

from config import settings
from shared.logging_config import setup_logging

setup_logging(settings.log_level)

import logging
logger = logging.getLogger(__name__)

async def notify_method(final_notif_data:Dict[str,Any],counter_notif:int)->Optional[bool]:
    try:
        notif_channel=final_notif_data['receiver_data']['channel']

        match notif_channel:
            case 'email':
                notif_result=await notify_by_email(final_notif_data,counter_notif)
            case 'sms':
                notif_result=await notify_by_email(final_notif_data,counter_notif)
            case 'call':
                notif_result=await notify_by_email(final_notif_data,counter_notif)
            case _:
                logger.warning('No notification channel specified, sending email instead')
                notif_result=await notify_by_email(final_notif_data,counter_notif)

        return notif_result
    
    except:
        logger.exception('Something went wrong while reading the notification channel')
        return None

async def send_notification(event_id:int,client:httpx.AsyncClient,counter_notif:int)->Optional[bool]:
    
    notification_data=await get_notification_data(event_id,client)
    
    if not notification_data:
        return None
    
    notif= await notify_method(notification_data,counter_notif)

    if not notif:
        return None
    
    return notif if notif else None