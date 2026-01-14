from DB.models.alarms import AlarmNotif,AlarmEvent,AlarmRule
from DB.models.measurements import Measurement
from DB.models.devices import Meter
from DB.models.roles import Project,ProjectAsignation,ProjectRecipient

from DB.database import async_session


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import Float, and_, func,desc, update, distinct
from typing import Dict, Any, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('notifier_services')

M3_MAPPING={ # Mapeo de constantes de mensaje PV-M3
    0:"serial_number",
    1: "vA", 2: "vB", 3: "vC", #Voltajes de cada línea
    4: "vAB", 5: "vBC", 6: "vCA", #Voltajes de cada fase
    7: "iA", 8: "iB", 9: "iC", #Corrientes de cada línea
    10: "PA", 11: "PB", 12: "PC", 13: "P", #Potencia Activa por línea y total
    14: "QA", 15: "QB", 16: "QC", 17: "Q", #Potencia Reactiva por línea y total
    18: "SA", 19: "SB", 20: "SC", 21: "S" , #Potencia Aparente por línea y total
    22: "PFA",23: "PFB",24: "PFC",25: "PF", #Factor de Potencia por línea y total
    26: "F", 27:"Signal_strength", #Frecuencia e intensidad de señal de transmisión
    28: "P_kWh_T", #Indication value of total positive active energy
    29: "R_kWh_T", #Indication value of total reverse active energy
    30: "P_kvarh_T", #Indication value of total positive reactive energy
    31: "R_kvarh_T", #Indication value of total reverse reactive energy
    32: "P_Active_demand", ##Demanda de potencia activa positiva actual
    33: "ICCID", #identificador único de placa
    34: "PT", #Valor de transformador de potencia del medidor
    35: "CT", #Valor de transformador de corriente del medidor (relación de transformación)
    ##A partir de aquí son las direcciones del segundo mensaje
    36: "TA", 37: "TB", 38: "TC", 39: "TN", #Temperaturas en líneas y neutro
    40: "iF", #Corriente de fuga
    41: "DI_status", #Estado de las entradas digitales (bit0:DI1,bit1:DI2,bit2:DI3,bit3:DI4)
    42: "P_kWh_A", 43: "R_kWh_A", #Energía activa en A: Positiva e Inversa/Reversa
    44: "P_kvarh_A", 45: "R_kvarh_A", #Energía reactiva en A: Positiva e Inversa/Reversa
    46: "P_kWh_B", 47: "R_kWh_B", #Energía activa en B: Positiva e Inversa/Reversa
    48: "P_kvarh_B", 49: "R_kvarh_B", #Energía reactiva en B: Positiva e Inversa/Reversa
    50: "P_kWh_C", 51: "R_kWh_C", #Energía activa en C: Positiva e Inversa/Reversa
    52: "P_kvarh_C", 53: "R_kvarh_C", #Energía reactiva en C: Positiva e Inversa/Reversa
    54: "THD_A", 55: "THD_B", 56: "THD_C" , #Rate de harmonicos de voltaje por línea
    57: "THDC_A",58: "THDC_B",59: "THDC_C", #Rate de harmonicos de corriente por línea
    60: "R_Active_demand", #Demanda de potencia activa inversa actual
    61: "P_Reactive_demand", #Demanda de potencia reactiva positiva actual
    62: "R_Reactive_demand", #Demanda de potencia reactiva inversa actual
    63: "V_unb", #Desbalance de voltaje en %
    64: "I_unb", #Desbalance de corriente en %
    65: "kWh_spike", #Energía total activa en "periodo spike"
    66: "kWh_peak", #Energía total activa en "periodo peak"
    67: "kWh_flat", #Energía total activa en "periodo flat"
    68: "kWh_valley", #Energía total activa en "periodo valley"
    69: "C1_kvarh", #Energía reactiva en 1er cuadrante
    70: "C2_kvarh", #Energía reactiva en 2do cuadrante
    71: "C3_kvarh", #Energía reactiva en 3er cuadrante
    72: "C4_kvarh"  #Energía reactiva en 4to cuadrante 
}

class EventEvaluator:
    async def check_notification_register(event_id: int)->Optional[Dict[str,Any]]:   
        try:  
            logger.info(f'Event ID received: {event_id}')

            async with async_session() as session:
                
                subquery = select(AlarmEvent.rule_id).where(AlarmEvent.id == event_id).scalar_subquery()
    
                stmt_notifs = (
                    select(AlarmNotif)
                    .join(AlarmEvent, AlarmNotif.rule_id== AlarmEvent.rule_id)
                    .where(AlarmEvent.rule_id == subquery)
                    .order_by(desc(AlarmNotif.last_notif))  
                    .limit(1)
                )

                result_notifs = await session.execute(stmt_notifs) #Ejecución del statement
                latest_notif = result_notifs.scalars().first() #Registro más reciente de las notificaciones encontradas

                await session.commit()
                
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
                
        except:
            logger.exception('The event has not being notified')
            return None
    
    async def get_triggers_ts(current_event:int,last_trigger_id:int,last_notif_id:int)->Optional[Dict[str,Any]]:
        """Recibo el id de la ultima vez que ocurrió lo mismo y de la ultima vez que eso fue notificado, para extraer en formato de fecha y hora"""
        
        try:  
            logger.info(f'Trigger: {last_trigger_id} Alarm: {last_notif_id}')

            async with async_session() as session:
                

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

                stmt_ts = (
                    select(Measurement.id,Measurement.timestamp)
                    .where(Measurement.id.in_(set(ids)))
                )

                result_ts = await session.execute(stmt_ts) #Ejecución del statement
                
                rows = {r.id: r for r in result_ts.mappings().all()}

                # reconstruyes respetando duplicados
                timestamp_results = [rows[i] for i in ids if i in rows]
    
                await session.commit()

                if not timestamp_results:
                    return None
                
                return timestamp_results
                
        except:
            logger.exception('No timestamps found for the triggers id')
            return None


class AlarmInformation:
    async def get_FKs(session:AsyncSession,event_id:int)-> Optional[Dict[str,int]]:
        try:
            stmt_FKs=(
                select(AlarmEvent)
                .where(AlarmEvent.id==event_id)
            )
            result_FKS=await session.execute(stmt_FKs)
            reg_FKS = result_FKS.scalars().first() 
            
            if not reg_FKS:
                logger.error(f"No event found with id {event_id}")
                return None
            
            return{
                    'rule_id':reg_FKS.rule_id,
                    'measure_id':reg_FKS.measure_id
                }
        
        except Exception as e:
            logger.error(f'Error obtaining the FKs: {e}')
            return None
        
    async def get_rule_details(session:AsyncSession,rule_id:int)-> Optional[Dict[str,Any]]:
        try:
            stmt_rule_inf=(
                select(AlarmRule)
                .where(AlarmRule.id==rule_id)
            )
            result_rule_inf=await session.execute(stmt_rule_inf)
            reg_rule = result_rule_inf.scalars().first() 
            
            if not reg_rule:
                logger.error(f"No rule found with id {rule_id}")
                return None
                
            return{
                    'parameter':reg_rule.parameter,
                    'comparator':reg_rule.comparator,
                    'threshold':reg_rule.threshold,
                    'level':reg_rule.level,
                    'comment':reg_rule.comment
                }

        except Exception as e:
            logger.error(f'Error obtaining the broken rule details: {e}')
            return None

    async def get_measure_details(session:AsyncSession,measure_id:int,parameter:str)-> Optional[Dict[str,Any]]:
        try:
            stmt_measure_inf=(
                select(Measurement)
                .where(Measurement.id==measure_id)
            )
            result_measure_inf=await session.execute(stmt_measure_inf)
            reg_measure = result_measure_inf.scalars().first() 
            
            if not reg_measure:
                logger.error(f"No measure found with id {measure_id}")
                return None
            
            if parameter not in reg_measure.parameters:
                logger.error(f"Parameter '{parameter}' not found in measure {measure_id}")
                return None

            return{
                    'ts':reg_measure.timestamp,
                    'meter_id':reg_measure.meter_id,
                    'reading':reg_measure.parameters[parameter]
                }

        except Exception as e:
            logger.error(f'Error obtaining the problematic measure details: {e}')
            return None

    async def get_event_details(event_id: int) -> Optional[Dict[str,Any]]:
        try:
            async with async_session() as session:
                #Obtener las FK del evento, una para measure y otra para rule
                event_fks=await AlarmInformation.get_FKs(session,event_id)
                if not event_fks:
                    logger.error(f'No fks given for event {event_id}')
                    return None
                
                #Obtener Comparador, umbral y severidad, parametro me ayuda a sacar info de la measure    
                rule_details=await AlarmInformation.get_rule_details(session,event_fks['rule_id']) 
                if not rule_details:
                    logger.error(f'No rule details found for rule')
                    return None
                
                #Obtener TS,Meter,reading
                if rule_details.get('parameter'):

                    final_param=M3_MAPPING[rule_details['parameter']]

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
            
        except Exception as e:
            logger.exception(f'Unexpected error getting details for event {event_id}')
            return None

    async def get_nicknames(meter_id:int)->Optional[Dict[str,Any]]:
        try:
            async with async_session() as session:
                stmt_nicknames=(
                    select(Meter.nickname.label("meter_nickname"),
                           Project.project_name.label("project_nickname"))
                    .join(Project, Project.id == Meter.project_id)
                    .where(Meter.id==meter_id)
                )
                result_nicknames=await session.execute(stmt_nicknames)
                nicknames=result_nicknames.mappings().first()
                
                await session.commit()

                if not nicknames:
                    return None

                return dict(nicknames)

        except Exception as e:
            logger.exception(f'Unexpected error getting the meter and project nicknames for {meter_id}')
            return None

    async def get_emails(meter_id:int)->Optional[List[str]]:
        try:
            async with async_session() as session:
                stmt_emails = (
                    select(distinct(ProjectRecipient.recipient_email))
                    .select_from(Meter)
                    .join(ProjectAsignation, ProjectAsignation.project_id == Meter.project_id)
                    .join(ProjectRecipient, ProjectRecipient.id == ProjectAsignation.recipient_id)
                    .where(Meter.id == meter_id)
                )
                result = await session.execute(stmt_emails)
                emails = result.scalars().all()
                
                await session.commit()

                return emails if emails else None

        except Exception as e:
            logger.exception(f'Unexpected error getting the recipients emails for meter {meter_id}')
            return None


class AlarmRegister:
    async def register_new_notification(new_notif:Dict[str,Any])->bool:
        
        async with async_session() as session:

            event_fks=await AlarmInformation.get_FKs(session,new_notif['event_id'])   

            logger.info(event_fks)
            
            new_notif_register=AlarmNotif(
                rule_id=event_fks['rule_id'],
                first_trigger=event_fks['measure_id'],
                last_trigger=event_fks['measure_id'],
                last_notif=event_fks['measure_id'],
                event_counter=new_notif['event_counter']
            )

            try:
                session.add(new_notif_register)
                await session.commit()
                return True
            
            except Exception as e:
                logger.error(f'Exception while saving on DB {e}')
                return False
            
    async def update_event_counter(update_info:Dict[str,Any])->bool:
        async with async_session() as session:
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
                await session.commit()
                
                if not update_result:
                    return None
                
                return {
                    'new_count':update_result.scalar_one_or_none()
                    }

            except Exception as e:
                logger.error(f'Exception while updating event counter DB {e}')
                return False
        
    async def update_notification_register(update_notification:Dict[str,Any]):
        async with async_session() as session:
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
                    return None

                stmt_update_notif_reg = (
                        update(AlarmNotif)
                        .where(AlarmNotif.id == update_notification['notif_id'])
                        .values(last_notif=current_event_measure)
                    )

                update_result=await session.execute(stmt_update_notif_reg)
                await session.commit()
                
                if not update_result:
                    return None
                
                return update_result

            except Exception as e:
                logger.error(f'Exception while updating event counter DB {e}')
                return False