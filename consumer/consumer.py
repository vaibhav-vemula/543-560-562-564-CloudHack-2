import time
import os
import requests
import json
import pika
time.sleep(20)

rmq = os.environ['RABBITMQ']
server_url = os.environ['SERVER_URL']
cname = os.environ['CNAME']

requests.post(server_url, json = {'cname':cname})

connection = pika.BlockingConnection(pika.URLParameters(rmq))
rmqch = connection.channel()
rmqch.queue_declare(queue='ride_match', durable=True)

def ackService(ch, method, properties, body):
    ride = json.loads(body)
    time.sleep(ride['time'])
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print('-----------------------------------------------')
    print("ID - ",cname, "\nData - ", ride)
    print('-----------------------------------------------')

rmqch.basic_qos(prefetch_count = 1)
rmqch.basic_consume(queue = 'ride_match', on_message_callback = ackService)
rmqch.start_consuming()