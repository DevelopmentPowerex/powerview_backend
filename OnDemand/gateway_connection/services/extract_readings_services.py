from DB.models.measurements import Measurement


from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

class Displayable_measurements:
    @staticmethod
    async def get_measures(meter_id:int,start_date:datetime,
                           end_date:datetime,
                           session: AsyncSession):
        
        try:                        
            stmt_measures = ( 
                select(Measurement)
                .where(and_(Measurement.meter_id == meter_id,
                            Measurement.timestamp>= start_date, 
                            Measurement.timestamp <= end_date))
            )
            
            result_measurements = await session.execute(stmt_measures)
            measures = result_measurements.scalars().all()

            return measures if measures else None

        except Exception:
            logger.exception('Something went wrong while extracting the measures')
