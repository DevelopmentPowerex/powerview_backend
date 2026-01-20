#Rutas API para el funcionamiento y conexión del uS
from AlwaysOn.uS_gateway.services.evaluate_readings_services import ReadingEvaluator

from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from DB.database import get_db

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/permanent/rule_evaluator", 
    tags=["Reading vs Rule Evaluator"]    
)

@router.get("/get_rules")
async def fetch_rules_from_db(measure_id:int = Query(..., gt=0),
                              session: AsyncSession = Depends(get_db)):
    try:
        rules_for_meter=await ReadingEvaluator.fetch_rules(measure_id,session)
        return rules_for_meter if rules_for_meter else []
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception:
        logger.exception("Unexpected error in getting the meter rules")
        raise HTTPException(500, detail="Internal server error")
    
@router.post("/save_new_event")
async def save_events(new_events:Dict[str,Any],
                      session: AsyncSession = Depends(get_db)):
    try:
        saved_result=await ReadingEvaluator.save_broken_rules(new_events,session)
        return saved_result      
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception:
        logger.exception("Unexpected error in save_new_reading")
        raise HTTPException(500, detail="Internal server error")