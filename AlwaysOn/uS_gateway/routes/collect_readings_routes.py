from AlwaysOn.uS_gateway.services.collect_readings_services import MQTTReadingCollector  # Importamos la clase
from AlwaysOn.uS_gateway.schemas import EntireMeasure

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from DB.database import get_db

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/permanent/reading_collector",  # Todas las rutas aquí empezarán con /mqtt
    tags=["MQTT Readings Collector"]    # Etiqueta para la documentación automática (Swagger/Redoc)
)
    
@router.post("/save_new_reading")
async def receive_lecture(lecture:EntireMeasure,
                          session: AsyncSession = Depends(get_db)): #Recibo la lectura procesada de parte del microservicio
    try:
        result = await MQTTReadingCollector.save_reading(lecture,session)
        return result 
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception:
        logger.exception("Unexpected error in save_new_reading")
        raise HTTPException(500, detail="Internal server error")




