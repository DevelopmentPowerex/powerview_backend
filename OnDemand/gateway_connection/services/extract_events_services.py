from DB.models.roles import Project
from DB.models.devices import  Meter
from DB.models.measurements import Measurement
from DB.models.alarms import AlarmNotif,AlarmRule

from sqlalchemy.orm import aliased

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from sqlalchemy import and_, case

from datetime import datetime

import logging
logger = logging.getLogger(__name__)

class Displayable_events:
    @staticmethod
    async def get_events(meter_list:List,
                         start_date:datetime,
                         end_date:datetime,
                         session:AsyncSession):

        try:

            m_first = aliased(Measurement)
            m_last = aliased(Measurement)

            stmt_events = (
                select(AlarmNotif)
                .join(AlarmRule, AlarmRule.id == AlarmNotif.rule_id)
                .join(m_first, m_first.id == AlarmNotif.first_trigger)
                .join(m_last,  m_last.id  == AlarmNotif.last_trigger)
                .where(
                    and_(
                        AlarmRule.meter_id.in_(meter_list),
                        and_(                                
                            m_first.timestamp.between(start_date, end_date),
                            m_last.timestamp.between(start_date, end_date)
                        )
                    )
                )
            )
            
            result_events = await session.execute(stmt_events)
            events = result_events.scalars().all()
            
            return events if events else None

        except Exception:
            logger.exception('Something went wrong while extracting the events')
    
    @staticmethod
    async def get_triggers_ts(first_trigger:int,
                              last_trigger:int,
                              session: AsyncSession):
        try:

            stmt_ts=(
                select(Measurement.timestamp)
                .where(Measurement.id.in_([first_trigger,last_trigger]))
                .order_by(
                    case(
                        (Measurement.id == first_trigger, 0),
                        (Measurement.id == last_trigger, 1),
                    )
                )
            )

            result_events = await session.execute(stmt_ts)
            events = result_events.scalars().all()

            return events if events else None

        except Exception:
            logger.exception('Something went wrong while extracting the timestamps')

    @staticmethod
    async def get_circuit_name(rule_id:int,
                               session: AsyncSession):
        try:
                
            stmt_name = (
                select(Project.project_name)
                .join(Meter, Meter.project_id == Project.id)   
                .join(AlarmRule, AlarmRule.meter_id == Meter.id) 
                .where(AlarmRule.id == rule_id)
            )
            result_name = await session.execute(stmt_name)
            name = result_name.scalar_one_or_none()
            
            return name if name else None

        except Exception:
            logger.exception(f'Something went wrong while extracting the circuit name for rule {rule_id}')
