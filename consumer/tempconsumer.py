import json
import pika
import time
import os
import requests

time.sleep(15)

# read rabbitmq connection url from environment variable
amqp_url = 'amqp://localhost:5672?connection_attempts=10&retry_delay=10'
# server_url = os.environ['SERVER_URL']
# consumer_id = os.environ['CONSUMER_ID']
url_params = pika.URLParameters(amqp_url)

# Send URL to consumer
# requests.post(server_url, data = consumer_id)

# connect to rabbitmq
connection = pika.BlockingConnection(url_params)
chan = connection.channel()

# declare a new queue
# in the rabbitmq volume even between restarts
chan.queue_declare(queue='ride_match', durable=True)


def receive_msg(ch, method, properties, body):
    # d = int(body.decode('utf-8'))
    # body = json.loads(body)
    # time.sleep(body['time'])
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("id", "time:",body )


# to make sure the consumer receives only one message at a time
chan.basic_qos(prefetch_count=1)

chan.basic_consume(queue='ride_match', on_message_callback=receive_msg)

chan.start_consuming()