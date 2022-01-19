import requests
import random
import schedule
from datetime import datetime
import time
import json
from paho.mqtt.client import Client

import pika, os



HTTP = "ipserver.json"
MQTT = "ipservermqtt.json"
CLIENT = Client(client_id="client_1")

url = os.environ.get('CLOUDAMQP_URL', 'amqps://qakmjopm:tL_k50XFtY7iMBJStupJ5M3d20DubMdB@jackal.rmq.cloudamqp.com/qakmjopm')

def sendAmqp(jsondata):
    y=''
    y = json.dumps(jsondata)
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel
    #channel.queue_declare(queue=f'DroneGianlucus/{jsondata["idDrone"]}') # Declare a queue
    channel.queue_declare(queue=f'DroneGianlucus/1')
    print(y)
    channel.basic_publish(exchange='DroneGianlucus',
                      routing_key=f'{jsondata["idDrone"]}',
                      body=y)

    print(f'jsondata["idDrone"]')
    connection.close()


def getIpHttp():
    f = open(HTTP, 'r')
    xx = f.read()
    myjson = json.loads(xx)
    f.close()
    return myjson['ip']


def getIpMqtt():
    f = open(MQTT, 'r')
    xx = f.read()
    myjson = json.loads(xx)
    f.close()
    return myjson['ip']


def postdronesend(jsondata):
    ip = getIpHttp()
    r = requests.post(f'http://{ip}:8011/api/drones', json=jsondata)


def error():
    print("errore orrore")


def mqttdronepublish(jsondata):
    ip = getIpMqtt()
    # ip="10.30.134.17:1833"
    # CLIENT.connect(ip)
    CLIENT.connect(ip, 1883, 60)
    print(jsondata["idDrone"])
    y = json.dumps(jsondata)
    CLIENT.publish(topic=f"DroneGianlucus/{jsondata['idDrone']}", payload=y)


# creo un metodo fittizio che simula il drone
def dronedemo():

    velocita = random.randrange(30000, 70000) / 1000
    posizione = random.randrange(30000, 70000) / 1000
    percentuale = random.randrange(1000, 100000) / 1000
    data = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    idDrone = random.randrange(1, 4)
    idPersona = random.randrange(1, 20)
    # print(data)
    json = {
        "dueDate": data,
        "idPersona": idPersona,
        "idDrone": idDrone,
        "posizione": posizione,
        "velocita": velocita,
        "percentuale": percentuale
    }

    sendAmqp(json)


if __name__ == '__main__':
    # eseguo
    #getIpMqtt()
    schedule.every(10).seconds.do(dronedemo)
    while True:
        schedule.run_pending()
        time.sleep(1)
