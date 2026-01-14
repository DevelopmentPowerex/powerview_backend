from AlwaysOn.uS_gateway.services.collect_readings_services import MQTTReadingCollector  # Importamos la clase
from AlwaysOn.uS_gateway.schemas import EntireMeasure

from fastapi import APIRouter, HTTPException
import json

router = APIRouter(
    prefix="/permanent/reading_collector",  # Todas las rutas aquí empezarán con /mqtt
    tags=["MQTT Readings Collector"]    # Etiqueta para la documentación automática (Swagger/Redoc)
)
    
@router.post("/save_new_reading/")
async def receive_lecture(lecture:EntireMeasure): #Recibo la lectura procesada de parte del microservicio
    try:
        result = await MQTTReadingCollector.save_reading(lecture)
        return result  
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




