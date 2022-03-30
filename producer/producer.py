import pika
import os
import time as t
import json
from flask import Flask
from flask import request

app = Flask(__name__)
port = 8000

rmq = os.environ['RABBITMQ']
connection = pika.BlockingConnection(pika.URLParameters(rmq))
rmqch = connection.channel()
rmqch.queue_declare(queue='database', durable=True)
rmqch.queue_declare(queue='ride_match', durable=True)

cl = []

@app.route('/')
def testGet():
    return "Flask Server running at" + str(port)

@app.route('/testpost', methods = ['POST'])
def testPost():
    return "Post Request Working"

@app.route('/new_ride', methods = ['POST'])
def new_ride():
    data = request.get_json()
    mess = json.dumps(data)
    print('-----------------------------------------------')
    print("Data Received - ",data)
    print('-----------------------------------------------')
    rmqch.basic_publish(routing_key = 'ride_match', body = mess, exchange='')
    rmqch.basic_publish(routing_key = 'database', body = mess,exchange='')
    time = str(data['time'])
    t.sleep(int(time))
    return "Ride Booked!! \n Happy Journey"

@app.route('/new_ride_matching_consumer', methods = ['POST'])
def matchRide():
    dat = request.get_json()
    print(dat)
    print(type(dat))
    print(dat['cname'])
    cip = request.remote_addr
    cl.append({"IP": cip, "Name": dat['cname']})
    return 'New Ride Matching Consumer Posted'

@app.route('/ride_logs')
def rideLogs():
    oo = {
        'data': cl
    }
    return oo

app.run(port=8000, host='0.0.0.0')