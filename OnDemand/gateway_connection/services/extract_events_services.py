from DB.models.roles import Project
from DB.models.devices import  Meter
from DB.models.measurements import Measurement
from DB.models.alarms import AlarmNotif,AlarmRule
from DB.models.devices import ParametersPVM3
from sqlalchemy.orm import aliased

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from sqlalchemy import and_

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
                select(Meter.nickname.label("circuit"),
                       AlarmRule.meter_id.label("meter_id"),
                       AlarmRule.comment.label("context"),
                       ParametersPVM3.param_code.label("parameter"),
                       AlarmRule.threshold,
                       AlarmRule.comparator,
                       AlarmRule.level,
                       m_first.timestamp.label('1st_ts'),
                       m_last.timestamp.label('last_ts'),
                       AlarmNotif.event_counter)

                .join(AlarmRule, AlarmRule.id == AlarmNotif.rule_id)
                .join(m_first, m_first.id == AlarmNotif.first_trigger)
                .join(m_last,  m_last.id  == AlarmNotif.last_trigger)
                .join(Meter, Meter.id == AlarmRule.meter_id)
                .join(ParametersPVM3,ParametersPVM3.id==AlarmRule.parameter)
                .where(
                    and_(
                        AlarmRule.meter_id.in_(meter_list),
                        and_(                                
                            m_first.timestamp.between(start_date, end_date),
                            m_last.timestamp.between(start_date, end_date)
                        )
                    )
                )
                .order_by(Meter.nickname, m_first.timestamp)
            )
            
            result_events = await session.execute(stmt_events)
            events = result_events.mappings().all()
            
            return events if events else None

        except Exception:
            logger.exception('Something went wrong while extracting the events')
    

