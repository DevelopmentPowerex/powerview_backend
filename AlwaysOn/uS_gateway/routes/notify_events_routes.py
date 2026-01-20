from AlwaysOn.uS_gateway.services.notify_events_services import EventEvaluator, AlarmInformation, AlarmRegister

from fastapi import APIRouter, HTTPException,Query, Depends

from typing import Any,Dict

from ..shared.routes_exceptions import handle_service_errors

from sqlalchemy.ext.asyncio import AsyncSession
from DB.database import get_db

router = APIRouter(
    prefix="/permanent/alarm_processing",  
    tags=["NOTIFIER SYSTEM"]  
)

import logging
logger = logging.getLogger(__name__)

@router.get("/check_alarm_register")
async def obtain_alarm_register(event_id:int = Query(..., gt=0),
                                session: AsyncSession = Depends(get_db)):
    try:
        notifs=await EventEvaluator.check_notification_register(session,event_id)
        return notifs 
    except Exception as e:
        handle_service_errors(logger, e)    

@router.get("/fetch_nicknames")
async def obtain_nicknames(meter_id:int = Query(..., gt=0),
                           session:AsyncSession = Depends(get_db)):
    try:
        nicknames=await AlarmInformation.get_nicknames(session,meter_id)
        return nicknames 
    except Exception as e:
        handle_service_errors(logger, e)

@router.get("/fetch_recipient_email")
async def obtain_emails(meter_id:int = Query(..., gt=0),
                        session:AsyncSession = Depends(get_db)):
    try:
        emails=await AlarmInformation.get_emails(session, meter_id)
        return emails
    except Exception as e:
        handle_service_errors(logger, e)

"""
@router.get("/fetch_recipient_number")
async def obtain_numbers(session:AsyncSession= Depends(get_db),
                         meter_id:int = Query(..., gt=0)):
    try:
        recipient_number=await AlarmInformation.get_numbers(session,meter_id)
        return recipient_number
    except Exception as e:
        handle_service_errors(logger, e)
"""

@router.get("/fetch_event_ts")
async def obtain_ts(current_event_id:int= Query(..., gt=0),
                    last_trigger_id:int= Query(..., gt=0), 
                    last_notif_id:int = Query(..., gt=0),
                    session:AsyncSession = Depends(get_db)):
    try:
        triggers_ts=await EventEvaluator.get_triggers_ts(session,current_event_id,last_trigger_id,last_notif_id)
        return triggers_ts
    except Exception as e:
        handle_service_errors(logger, e)

@router.get("/fetch_event_details")
async def obtain_event_details(details_for:int= Query(..., gt=0),
                               session:AsyncSession = Depends(get_db)):
    try:
        event_details=await AlarmInformation.get_event_details(session,details_for)
        return event_details  
    except Exception as e:
        handle_service_errors(logger, e)

@router.post("/register_notification")
async def create_notif_reg(new_reg:Dict[str,Any],
                           session:AsyncSession = Depends(get_db)): 
    try:
        return await AlarmRegister.register_new_notification(session,new_reg)
    except Exception as e:
        handle_service_errors(logger, e)
    
@router.post("/update_incidents_counter")
async def update_event_counter(update_info:Dict[str,Any],
                               session:AsyncSession = Depends(get_db)): 
    try:
        return await AlarmRegister.update_event_counter(session,update_info)
    except Exception as e:
        handle_service_errors(logger, e)
    
@router.post("/update_last_notif")
async def update_register(update_notif:Dict[str,Any],
                          session:AsyncSession = Depends(get_db)): 
    try:
        return await AlarmRegister.update_last_notification_register(session,update_notif)
    except Exception as e:
        handle_service_errors(logger, e)