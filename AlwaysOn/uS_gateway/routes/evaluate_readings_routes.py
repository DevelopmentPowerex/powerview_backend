#Rutas API para el funcionamiento y conexión del uS
from AlwaysOn.uS_gateway.services.evaluate_readings_services import ReadingEvaluator
from AlwaysOn.uS_gateway.schemas import EventModel

from fastapi import APIRouter, Query
from typing import Any

router = APIRouter(
    prefix="/permanent/rule_evaluator", 
    tags=["Reading vs Rule Evaluator"]    
)

@router.get("/get_rules")
async def fetch_rules_from_db(request:int = Query(..., gt=0)):
    rules_for_meter=await ReadingEvaluator.fetch_rules(request)
    return rules_for_meter if rules_for_meter else []
    
@router.post("/save_new_event")
async def save_events(new_events:dict[str,Any]):
    saved_result=await ReadingEvaluator.save_broken_rules(new_events)
    return saved_result      
