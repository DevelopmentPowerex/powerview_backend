
from DB.models.devices import Meter,ParametersPVM3
from DB.models.measurements import Measurement
from DB.database import async_session

from typing import Dict, Any, Optional, List

import logging
from sqlalchemy.future import select
from sqlalchemy import Float, and_, func

from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ext_measures')

class Displayable_measurements:
    async def get_measures(meter_id:int,start_date:datetime,end_date:datetime):
        
        try:
            async with async_session() as session:
                        
                stmt_measures = ( 
                    select(Measurement)
                    .where(and_(Measurement.meter_id == meter_id,
                                Measurement.timestamp>= start_date, 
                                Measurement.timestamp <= end_date))
                )
                
                result_measurements = await session.execute(stmt_measures)
                measures = result_measurements.scalars().all()

                return measures if measures else None

        except Exception as e:
            logger.error('Something went wrong while extracting the measures')
