# import required libraries
from tinydb import TinyDB
import pika
import os
import json

# read rabbitmq connection url from environment variable
amqp_url = 'amqp://localhost:5672?connection_attempts=10&retry_delay=10'
url_params = pika.URLParameters(amqp_url)

# connect to rabbitmq
connection = pika.BlockingConnection(url_params)
chan = connection.channel()

chan.queue_declare(queue='database', durable=True)

# create a local database
db = TinyDB('./tempdb.json')

def receive_msg(ch, method, properties, body):
    print(json.loads(body))
    bb = json.loads(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    db.insert(bb)


# to make sure the consumer receives only one message at a time
# next message is received only after acking the previous one
# chan.basic_qos(prefetch_count=1)

# define the queue consumption
chan.basic_consume(queue='database', on_message_callback=receive_msg)

chan.start_consuming()