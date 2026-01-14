from DB.models.alarms import AlarmRule, AlarmEvent
from DB.models.devices import Meter,ParametersPVM3
from DB.models.measurements import Measurement
from DB.enums import Comparators
from DB.database import async_session
from AlwaysOn.rabbit.rabbit_func import send_id

from typing import Dict, Any, Optional, List

import logging
from sqlalchemy.future import select
from sqlalchemy import Float, and_, func

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('GTW_evaluator')

class ReadingEvaluator:
    async def fetch_rules(measure_id: int) -> Optional[List[AlarmRule]]:
        try:  
            
            async with async_session() as session:
                
                stmt_rules = ( #Obtengo reglas dependiendo del medidor
                    select(AlarmRule)
                    .join(Measurement, AlarmRule.meter_id == Measurement.meter_id)
                    .where(Measurement.id == measure_id)
                    .order_by(AlarmRule.id)
                )

                result_rules = await session.execute(stmt_rules) #Ejecución del statement
                rules = result_rules.scalars().all()
                if not rules:
                    return None
                
                #Obtener los parametros de la medición a comparar (evitar enviar el JSON completo)
                
                required_params = [rule.parameter for rule in rules]
                

                stmt_param_codes = select(ParametersPVM3.id, ParametersPVM3.param_code).where(
                    ParametersPVM3.id.in_(required_params)
                )
                result_param_codes = await session.execute(stmt_param_codes)
                id_to_code = dict(result_param_codes.all())
                just_name=list(id_to_code.values())
                
                stmt_read_values=(
                    select(*[Measurement.parameters[name].astext.cast(Float) for name in just_name])
                    .where(Measurement.id==measure_id)
                )

                result_read_values = await session.execute(stmt_read_values) #Ejecución del statement
                read_values = result_read_values.first()
                
                if not read_values:
                    return None
                await session.commit()

                for rule in rules:
                    param_id=rule.parameter
                    rule.parameter=id_to_code[param_id]
                
                return {
                    "rules": rules,
                    "param_values": dict(zip(just_name, read_values))
                }
                
        except Exception as e:          
            logging.error(f"Error obtaining rules: {str(e)}")
            return None
        
    async def send_event_MQ(event_list:List[Any])->bool:
        try:    
            for event in event_list:                        
                await send_id('EV_SEND',event.id)
            return True
        except:
            return False
    
    async def save_broken_rules(events_info: dict[str,Any]) -> bool:
        try:
            async with async_session() as session:
                measure_events_id=events_info['measure_id']
                broken_rules=events_info['broken_rules']

                events_to_notif=[]

                for rule in broken_rules: #Por cada una de las reglas rotas se debe crear un registro
                    new_event= AlarmEvent(
                        measure_id = measure_events_id,
                        rule_id =rule
                    ) 
                    session.add(new_event)
                    events_to_notif.append(new_event) 

                await session.flush()  
                
                MQ_sent=await ReadingEvaluator.send_event_MQ(events_to_notif)

                if not MQ_sent:
                    logger.error("Error comms queue")
                    await session.rollback()
                    return False
                
                await session.commit()
                return True
            
        except Exception:
            logger.exception("Error saving alarm events")
            await session.rollback()
            return False
    