#Rutas API para el funcionamiento y conexión del uS
from OnDemand.gateway_connection.services.extract_readings_services import Displayable_measurements

from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from DB.database import get_db
from datetime import datetime
from typing import List
import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/displayable",  #Rutas dedicadas a la evaluación de reglas
    tags=["MEASURE EXTRACTION"]    # Etiqueta para la documentación automática (Swagger/Redoc)
)

@router.get("/fetch_circuits_for_report")
async def get_circuits_per_project(client_name:str=Query(...),
                                   project_name:str=Query(...),
                                   session:AsyncSession=Depends(get_db)):
    try:
        circuits=await Displayable_measurements.get_circuits(client_name,project_name,session)
        return circuits
    except Exception:
        logger.exception(f"Error fetching the circuits for {project_name}")

@router.get("/extract_measures")
async def obtain_measures(meters_ids: List[int] = Query(...), 
                          start_date:datetime=Query(...),
                          end_date:datetime=Query(...),
                          session: AsyncSession = Depends(get_db)):
    try:
        measurements=await Displayable_measurements.get_measures(meters_ids,start_date,end_date,session)
        return measurements
    except Exception:
        logger.exception("Error while getting the displayable measurements")
    
