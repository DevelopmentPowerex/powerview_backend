#Microservicio para comunicación entre PowerView y el broker MQTT

import asyncio
from typing import Dict, Any , Optional
import json
import httpx

from datetime import datetime, timedelta
from aiomqtt import Client, MqttError

import platform #Necesario para el funcionamiento del loop de windows
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from .protocols.pvm3 import M3_MAPPING

from dotenv import load_dotenv

load_dotenv("./AlwaysOn/uS/collector/.env.local")

from .config import settings
from .shared.logging_config import setup_logging

setup_logging(settings.log_level)

import logging
logger = logging.getLogger(__name__)

tasks=set()

unmixed_msg={}

def mixer(msgA,msgB)->Dict[str,Any]: 

    points_dict = {p["id"]: p["val"] for p in msgA}
    for p in msgB:
        points_dict[p["id"]] = p["val"]

    mixed_points = [{"id": k, "val": v} for k, v in sorted(points_dict.items())]
    
    return mixed_points

def decoder(message)->Optional[Dict[str,Any]]: 
    #Decodificación de mensaje real de PV-M3
    try:
        payload = message.payload.decode('utf-8') #Decodifica
        raw_data = json.loads(payload) 
        
        # Validación básica del mensaje
        if 'data' not in raw_data or not raw_data['data'] or 'tp' not in raw_data['data'][0] or 'point' not in raw_data['data'][0]:
            logger.warning("Something missing in MQTT message")
            return None
        
        #Separo el mensaje para poder acceder a sus partes
        data_entry = raw_data['data'][0]
        timestamp = data_entry['tp'] #El TS
        points = data_entry['point'] #Sus datos

        serial=points[0]['val'] #el numero serial siempre estará en el primer diccionario de la lista points
        key=f"{serial}-{timestamp}"
        
        is_first_half = any(p['id'] == 1 for p in points)

        if is_first_half:
            unmixed_msg[key] = points
            return None
        
        else:
            if key in unmixed_msg:
                existing_points = unmixed_msg.pop(key)
                mixed_points = mixer(existing_points, points)

                return {
                    "tp": timestamp,
                    "point": mixed_points
                }
            
    except Exception as e:
        logger.error(f"Error decodificando: {str(e)}")
        return None
    
def adjustTS(ts_og)->Optional[str]:
    try:
        ts_corregido = (ts_og // 1000) + (13 * 3600)
        dt=datetime.utcfromtimestamp(ts_corregido) - timedelta(hours=5)

        return str(datetime(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second
        ))
    except Exception as e:
        logger.warning(f'Timestamp error {e}')
        return None

def translate(meter_data)->Optional[Dict[str,Any]]:
    #Aquí los datos ya filtrados según su ID son traducidos según el protocolo de fábrica
    try:
        return {
            M3_MAPPING[p['id']]: p['val'] 
            for p in meter_data
            if p['id'] in M3_MAPPING
        }
    except Exception as exc:
        logger.error(f"Translation error: {str(exc)}")
        return None

def final_message(ts,message):
    meter=message.pop('serial_number')

    final_message={
        'serial_number':meter,
        'timestamp': ts,    
        'parameters':message
    }
    
    return final_message

async def send_measure(measurement_data: Dict[str, Any],httpx_client:httpx.AsyncClient):
   
    try:
        #Enviar datos de medición
        measurement_response = await httpx_client.post(
            f"{settings.gateway_url}/save_new_reading",
            json=measurement_data
        )
        measurement_response.raise_for_status()
        measurement_id=measurement_response.json()

        logger.info(f"sn: {measurement_data['serial_number']} | tp: {measurement_data['timestamp']} | reg: {measurement_id}")
    
    except httpx.HTTPError as e:
        logger.error(f"Error sending to gateway: {str(e)}")

async def process_message(msg,httpx_client:httpx.AsyncClient):
    try:
        #1) Decodificacion y unión de los mensajes (PV-M3 envia sus datos divididos en dos mensajes independientes)
        entry = decoder(msg)
        if not entry:
            return
        
        #2) Ajuste de ts
        ts_new=adjustTS(entry['tp']) #Funcion estandarizadora propia
        if not ts_new:
            return
        
        #4) Asignación de nombres
        decrypted=translate(entry['point']) #Los datos unidos se les asigna el nombre real del parámetro
        if not decrypted:
            return
        
        #5) Creación diccionarios
        measure = final_message(ts_new,decrypted)
        
        #6) Envío a gtw 
        await send_measure(measure,httpx_client)
    
    except Exception as exc:
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)

async def handle_message(msg,httpx_client:httpx.AsyncClient):
    task = asyncio.create_task(process_message(msg,httpx_client))
    tasks.add(task)
    task.add_done_callback(tasks.discard)  # Auto-eliminación al completarse

async def shutdown():
    logger.info("Shutting down, waiting for pending tasks...")
    if tasks: 
        try:
            await asyncio.wait(tasks, timeout=10.0)
        except asyncio.TimeoutError:
            logger.warning("Timeout waiting for tasks to complete")
    else:
        logger.info("No pending tasks to wait for")

async def main():
    while True:
        
        try:
            async with Client(
                hostname=settings.mqtt_broker, 
                port=settings.mqtt_port,
                identifier=settings.mqtt_identifier,
                timeout=settings.mqtt_timeout,
                clean_session=True
            ) as mqtt_client:
                
                await mqtt_client.subscribe(settings.mqtt_topic)
                logger.info(f"Subscribed to {settings.mqtt_topic}")
                async with httpx.AsyncClient(timeout=settings.gateway_timeout) as httpx_client:
                    async for message in mqtt_client.messages:

                        if len(tasks) > settings.tasks_max:
                            logger.warning("A lot of lectures are being processed, waiting...")
                            await asyncio.sleep(0.1)

                        await handle_message(message,httpx_client)

        except MqttError as e:
            logger.error(f"MQTT error: {e}")
            await asyncio.sleep(10)

if __name__=="__main__":
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.run(shutdown())