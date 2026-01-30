from DB.models.measurements import Measurement
from DB.models.devices import Meter,DeviceModel
from DB.models.roles import Project


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from datetime import datetime
from typing import List

from ...report_generator.protocols.auxiliar_info import PARAMETERS_FILTER

from sqlalchemy import select, and_, cast
from sqlalchemy.dialects.postgresql import ARRAY, TEXT

import logging
logger = logging.getLogger(__name__)

class Displayable_measurements:
    @staticmethod
    async def get_circuits(client_name:str,
                           project_order:str,
                           session: AsyncSession):
        try:                        
            stmt_circuits = ( 
                select(Meter.id,Meter.serial_number, Meter.nickname,DeviceModel.model_name)
                .join(DeviceModel, DeviceModel.id==Meter.model)
                .join(Project,Project.id==Meter.project_id)
                .where(Project.project_name==project_order)
            )
            
            result_circuits = await session.execute(stmt_circuits)
            circuits = result_circuits.mappings().all()

            return circuits if circuits else None

        except Exception:
            logger.exception('Something went wrong while extracting the circuits')

    @staticmethod
    async def get_measures(meters_ids:List[int],
                           start_date:datetime,
                           end_date:datetime,
                           session: AsyncSession):
        
        try:         
            desired_parameters = Measurement.parameters.op("-")(
                                cast(PARAMETERS_FILTER, ARRAY(TEXT))
                            ).label("reading")
            
            stmt_measures = ( 
                select(Meter.id,
                       Meter.nickname.label("circuit"),
                       Measurement.timestamp,
                       desired_parameters)
                .join (Meter,Meter.id==Measurement.meter_id)
                .where(
                        and_(
                            Measurement.meter_id.in_(meters_ids),
                            Measurement.timestamp.between(start_date, end_date),
                        )
                    )
                .order_by(Meter.nickname, Measurement.timestamp)
            )
            
            result_measurements = await session.execute(stmt_measures)
            measures = result_measurements.mappings().all()

            return measures if measures else None

        except Exception:
            logger.exception('Something went wrong while extracting the measures')
