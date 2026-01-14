#Rutas API para el funcionamiento y conexión del uS
from OnDemand.gateway_connection.services.extract_events_services import Displayable_events
from AlwaysOn.uS_gateway.services.notify_events_services import AlarmInformation

from AlwaysOn.uS_gateway.schemas import EventModel

from fastapi import APIRouter, HTTPException, Query
from typing import Optional,Any,List, Dict
import json
import logging
import asyncio

from datetime import datetime
from DB.database import async_session
import logging 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('events_router')

router = APIRouter(
    prefix="/displayable",  
    tags=["EVENTS EXTRACTION"]    
)

@router.get("/extract_events/")
async def obtain_events(meter_list: List[int] = Query(...), 
                        start_date:datetime= Query(...),
                        end_date:datetime= Query(...)):
    events=await Displayable_events.get_events(meter_list,start_date,end_date)
    return events if events else None

@router.get("/extract_rule_info/")
async def obtain_rule_details(rule_id:int =Query(...)):
    async with async_session() as session:
        rule_details= await AlarmInformation.get_rule_details(session,rule_id)
        return rule_details if rule_details else None

@router.get("/extract_triggers_ts/")
async def obtain_triggers_ts(first_trigger:int= Query(...),
                            last_trigger:int= Query(...)):
    triggers_ts=await Displayable_events.get_triggers_ts(first_trigger,last_trigger)
    return triggers_ts if triggers_ts else None


@router.get("/extract_circuit_name/")
async def obtain_circuit_name(rule_id:int= Query(...)):
    circuit_name=await Displayable_events.get_circuit_name(rule_id)
    return circuit_name if circuit_name else None