import asyncio
import logging
from typing import Dict, Any, Optional
import httpx

from AlwaysOn.rabbit.rabbit_func import read_id
from AlwaysOn.uS.notifier.check_notification_register import check_register
from AlwaysOn.uS.notifier.choose_notification_action import evaluate_register

from AlwaysOn.uS.notifier.update_register import update_counters
from AlwaysOn.uS.notifier.send_notification import send_notification
from AlwaysOn.uS.notifier.update_register import new_reg_notification, remind_event,update_counters

GATEWAY_URL = "http://127.0.0.1:8000/permanent/alarm_processing"  # URL del endpoint del gateway

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('notify_main') #Logger específico para Notificaciones

async def obtain_event_id()-> Optional[int]:#Obtener id de le medición a evaluar
    #Leer el último id publicado en el queue para alarmas de rabbit
    try:
        recent_event_id=await read_id('NOTIF') #Llamar a la función externa para obtener el id
        just_id=recent_event_id[0][recent_event_id[1]]
        logger.info(f"New alarm event: {just_id}")
        return just_id
    except Exception as e:
        logger.error(f'Error reading the id for the latest event {e}')
        return None
          
async def process_event(new_event_id:int,client:httpx.AsyncClient):
    
    registered_notification=await check_register(new_event_id,client) #Revisar si el evento está registrado o no
                  
    if registered_notification: 

        logger.info(f'Broken rule:{registered_notification["rule"]}. First event:{registered_notification["ft"]} Last event:{registered_notification["lt"]} #:{registered_notification["counter"]} Last Alarm:{registered_notification["ln"]}')      
        
        notify_decision= await evaluate_register(new_event_id,registered_notification,client) #Decidir si lo ocurrido debe notificarse o no 
        logger.info(f' Event has to be {notify_decision}')
        
        if (notify_decision != "Create") and (notify_decision is not None):
            
            new_counter= await update_counters(registered_notification['id'],new_event_id,client)
            
            if notify_decision=='Update': #Actualizar los contadores y no notificar
                return False,new_counter,registered_notification['id']
            
            elif notify_decision=='Remind': #Actualizar los contadores y notificar
                return True,new_counter,registered_notification['id']
              
    if (not registered_notification) or (notify_decision=='Create'):
        return True,1,None


async def main():
    async with httpx.AsyncClient() as client:
            while True:
                try:
                    new_event_id = await obtain_event_id() 
                    
                    if new_event_id:
                        
                        sender_trigger,notification_counter,previous_register_id=await process_event(new_event_id,client) 
                           
                        if sender_trigger:
                            sent_notification=await send_notification(new_event_id,client,notification_counter)
                            
                            if sent_notification:
                                if notification_counter != 1:
                                    event_proccessed= await remind_event(previous_register_id,new_event_id,client)   
                                else:
                                    event_proccessed= await new_reg_notification(new_event_id,notification_counter,client)   

                                
                        logger.info(f'Event {new_event_id} processed succesfully')

                except Exception as e:
                    logger.error(f'Unexpected error in main process: {e}')

if __name__=="__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt: Shutting down service")