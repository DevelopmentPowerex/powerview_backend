#Rutas API para el funcionamiento y conexión del uS
from OnDemand.gateway_connection.services.extract_events_services import Displayable_events
from AlwaysOn.uS_gateway.services.notify_events_services import AlarmInformation

from fastapi import APIRouter, Query, Depends
from typing import List
import logging

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from DB.database import get_db

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/report",  
    tags=["EVENTS EXTRACTION"]    
)

@router.get("/extract_events")
async def obtain_events(meter_list: List[int] = Query(...), 
                        start_date:datetime= Query(...),
                        end_date:datetime= Query(...),
                        session: AsyncSession = Depends(get_db)):
    try:
        events=await Displayable_events.get_events(meter_list,start_date,end_date,session)
        return events
    except Exception:
        logger.exception(f"Error while getting the events between {start_date} and {end_date}")
        return None
    
@router.get("/extract_rule_info")
async def obtain_rule_details(rule_id:int =Query(...),
                               session: AsyncSession = Depends(get_db)):
    try:
        rule_details= await AlarmInformation.get_rule_details(session,rule_id)
        return rule_details
    except Exception:
        logger.exception("Error while getting the rule details for the report")
        return None
    
@router.get("/extract_triggers_ts")
async def obtain_triggers_ts(first_trigger:int= Query(...),
                            last_trigger:int= Query(...),
                            session: AsyncSession = Depends(get_db)):
    try:
        triggers_ts=await Displayable_events.get_triggers_ts(first_trigger,last_trigger,session)
        return triggers_ts
    except Exception:
        logger.exception("Error getting the triggers timestamps")
        return None

