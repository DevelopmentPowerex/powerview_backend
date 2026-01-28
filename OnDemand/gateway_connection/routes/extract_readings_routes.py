#Rutas API para el funcionamiento y conexión del uS
from OnDemand.gateway_connection.services.extract_readings_services import Displayable_measurements

from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from DB.database import get_db
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/displayable",  #Rutas dedicadas a la evaluación de reglas
    tags=["MEASURE EXTRACTION"]    # Etiqueta para la documentación automática (Swagger/Redoc)
)

@router.get("/extract_measures/")
async def obtain_measures(meter_id:int, 
                          start_date:datetime,
                          end_date:datetime,
                          session: AsyncSession = Depends(get_db)):
    try:
        measurements=await Displayable_measurements.get_measures(meter_id,start_date,end_date,session)
        return measurements
    except Exception:
        logger.exception("Error while getting the displayable measurements")
    
