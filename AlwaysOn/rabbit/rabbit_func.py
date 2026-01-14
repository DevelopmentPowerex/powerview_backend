##Aquí están todas las funciones para trabajr con Rabbit como broker

import json
import aio_pika

URL_RABBIT="amqp://guest:guest@localhost/"

CONFIG = {
    'MQTT': {'queue': 'measure_pv', 'msg_key': 'new_measure_id'},
    'EV_RECV': {'queue': 'measure_pv', 'msg_key': 'new_measure_id'},

    'EV_SEND': {'queue': 'alarm_pv', 'msg_key': 'new_event_id'},
    'NOTIF': {'queue': 'alarm_pv', 'msg_key': 'new_event_id'},
}

##uS MQTT envía id de medición guardada para triggerear a uS Alm_EV
#requester: si lo envía uS MQTT o Alm_EV
async def send_id(requester:str,desired_id: int):
    
    conf = CONFIG.get(requester)
    
    if not conf:
        print("Invalid requester")
        return
    
    connection = await aio_pika.connect_robust(URL_RABBIT)

    async with connection:

        channel = await connection.channel()
        queue = await channel.declare_queue(conf['queue'], durable=True)

        message = aio_pika.Message(
            body=json.dumps({conf['msg_key']: desired_id}).encode()
        )

        await channel.default_exchange.publish(
            message, routing_key=conf['queue']
        )

##uS Alm_EV debe estar pendiente de las nuevas escrituras en la misma queue
async def read_id(requester:str):
    
    conf = CONFIG.get(requester)

    if not conf:
        print("Invalid requester")
        return
    
    connection = await aio_pika.connect_robust(URL_RABBIT)
    channel = await connection.channel()
    queue = await channel.declare_queue(conf['queue'], durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body.decode())
                return (data,conf['msg_key'])
