"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 23/11/2019

Aplicacao que tem por objetivo realizar a conexao com o servidor MQTT e publicar uma informacao nessa rede
Esta aplicacao eh instanciada pela aplicacao Web DJANGO
"""

import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime

#====================================================
# MQTT Settings
#MQTT_Broker = "192.168.0.11"
MQTT_Broker = "10.0.1.1"
MQTT_Port = 1883
Keep_Alive_Interval = 45
#====================================================

def on_connect(client, userdata, rc):
	if rc != 0:
		pass
		print("Unable connect to MQTT Server !!!")
	else:
		print("Connected with MQTT Server: " + str(MQTT_Broker))

def on_publish(client, userdata, mid):
	pass

def on_disconnect(client, userdata, rc):
	if rc !=0:
		pass


def publish_To_Topic(topic, message):
	mqttc = mqtt.Client()
	mqttc.on_connect = on_connect
	mqttc.on_disconnect = on_disconnect
	mqttc.on_publish = on_publish
	mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
	mqttc.publish(topic, message)
	print("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
	print("")
	mqttc.disconnect()