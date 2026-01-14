#Rutas API para el funcionamiento y conexión del uS
from OnDemand.gateway_connection.services.extract_readings_services import Displayable_measurements
from AlwaysOn.uS_gateway.schemas import EventModel

from fastapi import APIRouter, HTTPException, Query
from typing import Optional,Any,Dict
import json
import logging
import asyncio

from datetime import datetime

import logging 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('measure_route')

router = APIRouter(
    prefix="/displayable",  #Rutas dedicadas a la evaluación de reglas
    tags=["MEASURE EXTRACTION"]    # Etiqueta para la documentación automática (Swagger/Redoc)
)

@router.get("/extract_measures/")
async def obtain_measures(meter_id:int, start_date:datetime,end_date:datetime):
    measurements=await Displayable_measurements.get_measures(meter_id,start_date,end_date)
    return measurements if measurements else None
    
