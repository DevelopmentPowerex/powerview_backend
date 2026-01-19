import httpx
from typing import Optional, Dict, Any,List

from datetime import datetime

import logging
from .config import settings
from .protocols.endpoints import GET_EVENT_TIMESTAMPS

logger = logging.getLogger(__name__)

async def fetch_events_timestamps(event_id:int,notif_reg_data:Dict[str,Any],client:httpx.AsyncClient)->Optional[List[Dict[str,Any]]]:
    try:
        notification_triggers_ts = await client.get(
                f"{settings.gateway_url}{GET_EVENT_TIMESTAMPS}",
                params={"current_event_id":event_id,"last_trigger_id":notif_reg_data['lt'], "last_notif_id":notif_reg_data['ln']}
        )
 
        notification_triggers_ts.raise_for_status()
        timestamps_per_id=notification_triggers_ts.json() #Lista de diccionarios de {id:int,timestamp: str iso}

        return timestamps_per_id if timestamps_per_id else None
    
    except Exception as e:
        logger.error(f'Error obtaining the timestamps of the relevant events {e}')
        return None

async def calculate_time_between_events(relevant_events_ts:List[Dict[str,Any]]):
    try:
        new_event_ts=datetime.fromisoformat(relevant_events_ts[0]['timestamp'])
        last_trigger_ts=datetime.fromisoformat(relevant_events_ts[1]['timestamp'])
        last_notif_ts=datetime.fromisoformat(relevant_events_ts[2]['timestamp'])
        
        diff_ne_lt=((new_event_ts-last_trigger_ts).total_seconds())/60 #Diferencia de tiempo entre el evento evaluado y la última vez que se rompió esta regla en minutos
        diff_ne_ln=((new_event_ts-last_notif_ts).total_seconds())/60 #Diferencia de tiempo entre el evento evaluado y la última vez que se notificó en minutos

        return {
            'event_vs_last_trigger':diff_ne_lt,
            'event_vs_last_notif':diff_ne_ln,
        }
    except Exception as e: 
        logger.error(f"Error calculating the time between relevant events {e}")
        return None
    
async def evaluate_register(event_id:int,notif_reg_data:Dict[str,Any],client:httpx.AsyncClient)->Optional[str]: #Revisa el registro previo del evento para saber qué hacer
    #logger.info(f' Última notificación registrada: {notif_reg_data}')
    #1ro obtener los timestamps para poder comparar los tiempos
    relevant_events_ts=await fetch_events_timestamps(event_id,notif_reg_data,client)
    if not relevant_events_ts:
        return None
    
    #Timestamp del evento actual, Timestamp de la última vez que ocurrió, Timestamp de la última vez que se notificó
    logger.debug (f' CE tp: {relevant_events_ts[0]}, LT tp: {relevant_events_ts[1]}, LN tp: {relevant_events_ts[2]}')

    #2do calcular cuanto tiempo ha pasado entre el evento nuevo y los triggers relevantes
    time_differences=await calculate_time_between_events(relevant_events_ts)
    if not time_differences:
        return None
    
    logger.debug (f'Time between events: {time_differences}')

    #3ro comparar los tiempos resultados con los tiempos establecidos de decisión

    ###################################################################################################################
    #AQUI ACOPLAR SISTEMA DE TIEMPO DE NOTIFICACIÓN PERSONALIZADO (LOW_PRIO)###########################################
    ###################################################################################################################
    time_notif=5 #5 min de espera para volver a enviar una notificación
    time_new_event=15 #Debe ser tomado como un evento nuevo desde cero
    
    time_last_trigger=time_differences.get('event_vs_last_trigger') #Hace cuanto saltó el último trigger (Incluso sin ser notificado)
    time_last_notif=time_differences.get('event_vs_last_notif') #Hace cuánto fue la última notificación

    try: 
        if time_last_trigger>=time_new_event: 
            return "Create"

        if time_last_notif<time_notif: #Hay que actualizar el contador de eventos y el trigger pero no notificar
            return 'Update'
        
        elif time_last_notif>=time_notif: #Hay que actualizar el contador, trigger y notificar otra vez
            return 'Remind'
    except Exception as e:
        logger.error(f"Error deciding what to do, creating new notification instead {e}")
        return "Create"

