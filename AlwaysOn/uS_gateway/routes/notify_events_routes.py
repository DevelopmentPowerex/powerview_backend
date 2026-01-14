from AlwaysOn.uS_gateway.services.notify_events_services import EventEvaluator, AlarmInformation, AlarmRegister
from AlwaysOn.uS_gateway.schemas import NotifModel

from fastapi import APIRouter, HTTPException,Query

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional,Any,Dict

router = APIRouter(
    prefix="/permanent/alarm_processing",  
    tags=["NOTIFIER SYSTEM"]  
)

@router.get("/check_alarms_register/")
async def obtain_notifs(event_id:int = Query(..., gt=0)):
    notifs=await EventEvaluator.check_notification_register(event_id)
    return notifs 

@router.get("/fetch_nicknames/")
async def obtain_nicknames(meter_id:int = Query(..., gt=0)):
    notifs=await AlarmInformation.get_nicknames(meter_id)
    return notifs 

@router.get("/fetch_recipients_email/")
async def obtain_emails(meter_id:int = Query(..., gt=0)):
    emails=await AlarmInformation.get_emails(meter_id)
    return emails

@router.get("/fetch_recipients_number/")
async def obtain_numbers(meter_id:int = Query(..., gt=0)):
    notifs=await AlarmInformation.get_numbers(meter_id)
    return notifs 

@router.get("/fetch_events_ts/")
async def obtain_ts(current_event_id:int,last_trigger_id:int, last_notif_id:int = Query(..., gt=0)):
    triggers_ts=await EventEvaluator.get_triggers_ts(current_event_id,last_trigger_id,last_notif_id)
    return triggers_ts

@router.get("/fetch_event_details/")
async def event_details(details_for:int):
    details=await AlarmInformation.get_event_details(details_for)
    return details  

@router.post("/register_notification/")
async def notify(new_reg:Dict[str,Any]): 
    try:
        return await AlarmRegister.register_new_notification(new_reg)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/update_register/")
async def notify(update_info:Dict[str,Any]): 
    try:
        return await AlarmRegister.update_event_counter(update_info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/reminder_update/")
async def notify(update_notif:Dict[str,Any]): 
    try:
        return await AlarmRegister.update_notification_register(update_notif)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))