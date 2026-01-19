from DB.models.alarms import AlarmNotif,AlarmEvent,AlarmRule
from DB.models.measurements import Measurement
from DB.models.devices import Meter
from DB.models.roles import Project,ProjectAsignation,ProjectRecipient

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import Float, and_, func,desc, update, distinct
from typing import Dict, Any, Optional, List

import logging
logger = logging.getLogger(__name__)

from ..protocols.pvm3 import M3_MAPPING

class EventEvaluator:
    @staticmethod
    async def check_notification_register(session:AsyncSession, event_id: int)->Optional[Dict[str,Any]]:   
        try:  
            logger.debug(f'Event ID received: {event_id}')

            stmt_notifs = (
                select(AlarmNotif)
                .join(AlarmEvent, AlarmEvent.rule_id == AlarmNotif.rule_id)
                .where(AlarmEvent.id == event_id)
                .order_by(desc(AlarmNotif.last_notif))
                .limit(1)
            )

            result_notifs = await session.execute(stmt_notifs) #Ejecución del statement
            latest_notif = result_notifs.scalars().first() #Registro más reciente de las notificaciones encontradas
            
            if not latest_notif:
                return None
            
            already_reg={
                'id':latest_notif.id,
                'rule': latest_notif.rule_id,
                'ft':latest_notif.first_trigger,
                'lt':latest_notif.last_trigger,
                'ln':latest_notif.last_notif,
                'counter':latest_notif.event_counter
            }

            return  already_reg
                
        except Exception:
            logger.exception("Error checking notification register. event_id=%s", event_id)
            return None


    @staticmethod
    async def get_triggers_ts(session:AsyncSession, current_event:int,last_trigger_id:int,last_notif_id:int)->Optional[List[Dict[str,Any]]]:
        """Recibo el id de la ultima vez que ocurrió lo mismo y de la ultima vez que eso fue notificado, para extraer en formato de fecha y hora"""
        
        try:  
            logger.debug(f'Trigger: {last_trigger_id} Alarm: {last_notif_id}')

            stmt_current = (
                select(Measurement.id)
                .join(AlarmEvent, AlarmEvent.measure_id == Measurement.id)
                .where(AlarmEvent.id==current_event)
                .limit(1)
                )

            result_current = await session.execute(stmt_current)
            current_event_measure = result_current.scalar_one_or_none()

            if not current_event_measure:
                return None

            ids = [current_event_measure, last_trigger_id, last_notif_id]
            ids = [i for i in ids if i is not None]

            if len(ids) < 3:
                return None
            
            stmt_ts = (
                select(Measurement.id,Measurement.timestamp)
                .where(Measurement.id.in_(set(ids)))
            )

            result_ts = await session.execute(stmt_ts) #Ejecución del statement
            
            rows = {r["id"]: r for r in result_ts.mappings().all()}

            # reconstruyes respetando duplicados
            timestamp_results = [dict(rows[i]) for i in ids if i in rows]

            if (not timestamp_results) or (len(timestamp_results) != 3):
                return None
            
            return timestamp_results
                
        except Exception:
            logger.exception(
                "No timestamps found for triggers. current_event=%s last_trigger_id=%s last_notif_id=%s",
                current_event, last_trigger_id, last_notif_id
            )
            return None

class AlarmInformation:
    @staticmethod
    async def get_FKs(session:AsyncSession,event_id:int)-> Optional[Dict[str,int]]:
        try:
            stmt_FKs=(
                select(AlarmEvent.rule_id, AlarmEvent.measure_id)
                .where(AlarmEvent.id==event_id)
            )
            result_FKS=await session.execute(stmt_FKs)
            reg_FKS = result_FKS.mappings().first()
            
            if not reg_FKS:
                return None
            
            return{
                    'rule_id':reg_FKS['rule_id'],
                    'measure_id':reg_FKS['measure_id']
                }
        
        except Exception:
            logger.exception("Error obtaining FKs. event_id=%s", event_id)
            return None
    
    @staticmethod   
    async def get_rule_details(session:AsyncSession,rule_id:int)-> Optional[Dict[str,Any]]:
        try:
            stmt_rule_inf=(
                select(AlarmRule.parameter,
                       AlarmRule.comparator,
                       AlarmRule.threshold,
                       AlarmRule.level,
                       AlarmRule.comment)
                .where(AlarmRule.id==rule_id)
            )
            result_rule_inf=await session.execute(stmt_rule_inf)
            reg_rule = result_rule_inf.mappings().first() 
            
            if not reg_rule:
                logger.error(f"No rule found with id {rule_id}")
                return None
                
            return{
                    'parameter':reg_rule.get("parameter"),
                    'comparator':reg_rule.get("comparator"),
                    'threshold':reg_rule.get("threshold"),
                    'level':reg_rule.get("level"),
                    'comment':reg_rule.get("comment")
                }

        except Exception:
            logger.exception('Error obtaining the broken rule details')
            return None

    @staticmethod
    async def get_measure_details(session:AsyncSession,measure_id:int,parameter:str)-> Optional[Dict[str,Any]]:
        try:
            stmt_measure_inf=(
                select(Measurement.timestamp,
                       Measurement.meter_id,
                       Measurement.parameters)
                .where(Measurement.id==measure_id)
            )
            result_measure_inf=await session.execute(stmt_measure_inf)
            reg_measure = result_measure_inf.mappings().first() 
            
            if not reg_measure:
                logger.error(f"No measure found with id {measure_id}")
                return None
            
            ext_parameters=reg_measure.get("parameters") or {}

            if parameter not in ext_parameters:
                logger.error(f"Parameter '{parameter}' not found in measure {measure_id}")
                return None

            return{
                    'ts':reg_measure.get("timestamp"),
                    'meter_id':reg_measure.get("meter_id"),
                    'reading':ext_parameters[parameter]
                }

        except Exception:
            logger.exception('Error obtaining the problematic measure details')
            return None

    @staticmethod
    async def get_event_details(session:AsyncSession,event_id: int) -> Optional[Dict[str,Any]]:
        try:
            measure_details = None
           
            #Obtener las FK del evento, una para measure y otra para rule
            event_fks=await AlarmInformation.get_FKs(session,event_id)
            if not event_fks:
                logger.error(f'No fks given for event {event_id}')
                return None
            
            #Obtener Comparador, umbral y severidad, parametro me ayuda a sacar info de la measure    
            rule_details=await AlarmInformation.get_rule_details(session,event_fks['rule_id']) 
            if not rule_details:
                logger.error("No rule details found for rule %s", event_fks.get("rule_id"))
                return None
            
            #Obtener TS,Meter,reading
            if rule_details.get('parameter'):

                final_param=M3_MAPPING.get(rule_details['parameter'])

                if not final_param:
                    logger.error("No M3 mapping for parameter %s", rule_details.get("parameter"))
                    return None

                measure_details=await AlarmInformation.get_measure_details(
                    session,
                    event_fks['measure_id'],
                    final_param
                )
                if not measure_details:
                    logger.error(f'No measure details found for measure')
                    return None

            if not all([measure_details, rule_details]):
                return None

            final_details={
                'ts':measure_details['ts'],
                'meter_id':measure_details['meter_id'],
                'parameter':rule_details['parameter'],
                'comparator':rule_details['comparator'],
                'threshold':rule_details['threshold'],
                'reading':measure_details['reading'],
                'level':rule_details['level'],
                'comment':rule_details['comment']
            }

            return final_details
            
        except Exception:
            logger.exception('Unexpected error getting details for event')
            return None

    @staticmethod
    async def get_nicknames(session:AsyncSession,meter_id:int)->Optional[Dict[str,Any]]:
        try:
            
            stmt_nicknames=(
                select(Meter.nickname.label("meter_nickname"),
                        Project.project_name.label("project_nickname"))
                .join(Project, Project.id == Meter.project_id)
                .where(Meter.id==meter_id)
            )
            result_nicknames=await session.execute(stmt_nicknames)
            nicknames=result_nicknames.mappings().first()
            
            if not nicknames:
                return None

            return dict(nicknames)

        except Exception:
            logger.exception('Unexpected error getting the meter and project nicknames')
            return None

    @staticmethod
    async def get_emails(session:AsyncSession, meter_id:int)->Optional[List[str]]:
        try:
            stmt_emails = (
                select(distinct(ProjectRecipient.recipient_email))
                .select_from(Meter)
                .join(ProjectAsignation, ProjectAsignation.project_id == Meter.project_id)
                .join(ProjectRecipient, ProjectRecipient.id == ProjectAsignation.recipient_id)
                .where(Meter.id == meter_id)
            )
            result = await session.execute(stmt_emails)
            emails = result.scalars().all()
            
            return emails if emails else None

        except Exception:
            logger.exception('Unexpected error getting the recipients emails')
            return None

class AlarmRegister:
    @staticmethod
    async def register_new_notification(session:AsyncSession,new_notif:Dict[str,Any])->bool:
        
        event_fks=await AlarmInformation.get_FKs(session,new_notif.get('event_id'))   

        if event_fks is None:
            raise ValueError("Required Foreign Keys are missing")
        
        new_notif_register=AlarmNotif(
            rule_id=event_fks.get('rule_id'),
            first_trigger=event_fks.get('measure_id'),
            last_trigger=event_fks.get('measure_id'),
            last_notif=event_fks.get('measure_id'),
            event_counter=new_notif.get('event_counter')
        )

        try:
            session.add(new_notif_register)
            await session.commit()
            
            return True
        
        except Exception:
            logger.exception('Exception while saving on DB')
            return False
    
    @staticmethod
    async def update_event_counter(session:AsyncSession,update_info:Dict[str,Any])->Optional[Dict[str,Any]]:

        try:
            stmt_current = (
                    select(Measurement.id)
                    .join(AlarmEvent, AlarmEvent.measure_id == Measurement.id)
                    .where(AlarmEvent.id==update_info['event_id'])
                    .limit(1)
                    )

            result_current = await session.execute(stmt_current)
            current_event_measure = result_current.scalar_one_or_none()

            if not current_event_measure:
                return None

            stmt_update = (
                update(AlarmNotif)
                .where(AlarmNotif.id == update_info['notif_id'])
                .values(event_counter=AlarmNotif.event_counter+1,
                        last_trigger=current_event_measure
                        )
                .returning(AlarmNotif.event_counter)
            )

            update_result=await session.execute(stmt_update)
            new_counter=update_result.scalar_one_or_none()

            await session.commit()
            
            if new_counter is None:
                return None
            
            return {
                'new_count':new_counter
                }

        except Exception:
            logger.exception('Exception while updating event counter DB')
            return None
    
    @staticmethod
    async def update_last_notification_register(session:AsyncSession,update_notification:Dict[str,Any])->bool:
        try:
            stmt_current = (
                            select(Measurement.id)
                            .join(AlarmEvent, AlarmEvent.measure_id == Measurement.id)
                            .where(AlarmEvent.id==update_notification['event_id'])
                            .limit(1)
                            )

            result_current = await session.execute(stmt_current)
            current_event_measure = result_current.scalar_one_or_none()

            if not current_event_measure:
                return False

            stmt_update_notif_reg = (
                    update(AlarmNotif)
                    .where(AlarmNotif.id == update_notification['notif_id'])
                    .values(last_notif=current_event_measure)
                    .returning(AlarmNotif.id)
                )

            update_result=await session.execute(stmt_update_notif_reg)
            updated_id=update_result.scalar_one_or_none()
            
            await session.commit()
            
            return updated_id is not None

        except Exception:
            logger.exception('Exception while updating event counter DB')
            return False
            