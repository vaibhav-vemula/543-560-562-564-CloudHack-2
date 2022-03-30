import pika
import os
import json
from tinydb import TinyDB

db = TinyDB('./ridesDB.json')

rmq = os.environ['RABBITMQ']
connection = pika.BlockingConnection(pika.URLParameters(rmq))
rmqch = connection.channel()
rmqch.queue_declare(queue='database', durable=True)

def insertRide(ch, method, properties, body):
    ride = json.loads(body)
    db.insert(ride)
    ch.basic_ack(delivery_tag=method.delivery_tag)

rmqch.basic_qos(prefetch_count = 1)
rmqch.basic_consume(queue = 'database', on_message_callback = insertRide)
rmqch.start_consuming()