# import required libraries
import pika
import os
from flask import Flask
from flask import request
import time as t
import json

# Array to store new consumer
consumer_list = []

# read rabbitmq connection url from environment variable
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

# connect to rabbitmq
connection = pika.BlockingConnection(url_params)
chan = connection.channel()

# initialise queues
chan.queue_declare(queue='ride_match', durable=True)
chan.queue_declare(queue='database', durable=True)

# initialise app
app = Flask(__name__)


@app.route('/')
def hello():
    return "HELLO"

# ride matching 
@app.route('/new-ride', methods = ['POST'])
def new_ride():
    data = request.get_json()
    mess = json.dumps(data)
    print("GOT DATA",data)
    chan.basic_publish(
        routing_key = 'ride_match', 
        body = mess,
        exchange='',
    )
    chan.basic_publish(
        routing_key = 'database', 
        body = mess,
        exchange='',
    )
    # time = str(data['time'])
    # t.sleep(int(time))
    return "Success"

@app.route('/new_ride_matching_consumer')
def ride_matching():
    print(request.data)
    consumer_id = request.data.consumer_id
    consumer_ip = request.remote_addr
    consumer_list.append({
        "name": consumer_id,
        "ip": consumer_ip,
    })

print("Starting server")
app.run(port=5005, host='0.0.0.0')