from AlwaysOn.rabbit.rabbit_func import send_id
from DB.models.measurements import Measurement
from DB.models.devices import Meter
from AlwaysOn.uS_gateway.schemas import EntireMeasure
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from ..config import settings

from typing import Optional

import logging
logger = logging.getLogger(__name__)

class MQTTReadingCollector:

    @staticmethod
    async def save_reading(lecture: EntireMeasure,session:AsyncSession) -> Optional[int]: 

        try:
            #Obtener el id del medidor que quiere guardar la lectura
            idReadMeter = await session.scalar(
                select(Meter.id).where(Meter.serial_number == lecture.serial_number)
            )

            if not idReadMeter:
                logger.error(f'Meter with SN: {lecture.serial_number} not registered')
                return None

            #Guardar la lectura según su medidor correspondiente
            new_measurement= Measurement(
                meter_id=idReadMeter,
                timestamp=lecture.timestamp,
                parameters=lecture.parameters
            )
        
            session.add(new_measurement)
            await session.flush()
            await session.commit() 

        except Exception:
            logger.exception("Error saving reading on DB")
            await session.rollback()
            return None

        try: #Envío a Rabbit como trigger para el evaluador
            await send_id('MQTT',new_measurement.id, settings.rabbit_url)
        except Exception:
            logger.exception("Error on uS comms")

        return new_measurement.id