import pika
import time
import os
import requests
import json
time.sleep(20)

rmq = os.environ['RABBITMQ']
server_url = os.environ['SERVER_URL']
cid = os.environ['CID']

requests.post(server_url, data = cid)

connection = pika.BlockingConnection(pika.URLParameters(rmq))
rmqch = connection.channel()
rmqch.queue_declare(queue='ride_match', durable=True)

def ackService(ch, method, properties, body):
    ride = json.loads(body)
    time.sleep(ride['time'])
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print("ID - ",cid, "\ndata - ", ride)

rmqch.basic_qos(prefetch_count=1)
rmqch.basic_consume(queue='ride_match', on_message_callback = ackService)
rmqch.start_consuming()