from AlwaysOn.rabbit.rabbit_func import send_id
from DB.models.measurements import Measurement
from DB.models.devices import Meter
from DB.database import async_session
from AlwaysOn.uS_gateway.schemas import EntireMeasure

from sqlalchemy import select
from ..config import settings

import logging
logger = logging.getLogger(__name__)

class MQTTReadingCollector:

    @staticmethod
    async def save_reading(lecture: EntireMeasure) -> bool: 
        try:
            async with async_session() as session:
                try:
                     # 1. Obtener ID del medidor
                    idReadMeter = await session.scalar(
                        select(Meter.id).where(Meter.serial_number == lecture.serial_number)
                    )
                    if not idReadMeter:
                        logger.error(f'Meter with SN: {lecture.serial_number} not registered')
                        return False
                
                except Exception as e:
                    logger.error(f'Error looking for SN: {lecture.serial_number} → {e}')
                    return

                new_measurement= Measurement(
                    meter_id=idReadMeter,
                    timestamp=lecture.timestamp,
                    parameters=lecture.parameters
                )
                
                try:
                    session.add(new_measurement)
                    await session.commit() #Final de microservicio 
                
                    try: #Envío a Rabbit como trigger para el evaluador
                        await send_id('MQTT',new_measurement.id, settings.rabbit_url)
                    except:
                        logger.error("Error comms queue")
                    return True
                except:
                    logger.error("Error committing")
                    return False
        except:
            logger.error("Error saving measurement")
            await session.rollback()
            return False
    





