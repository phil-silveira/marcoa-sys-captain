"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 19/11/2019

Aplicacao responsavel por realizar diversas operacoes referente ao MQTT
Para os dados recebidos via MQTT para o quadro de comando, decodifica a mensagem
e armazena o respectivo valor no banco de dados
"""
import paho.mqtt.client as mqtt
from db_config import connection
from db_store import *
from WeatherData import WeatherData
from publish import publish_To_Topic

# Assinando o TOPIC e definindo o Broker e sua Respectiva porta
mqtt_topic = "qc1/#"
#mqtt_broker_ip = "192.168.0.11"
mqtt_broker_ip = "10.0.1.1"
mqtt_broker_port = 1883

client = mqtt.Client()

# Esta Funcao se conecta ao Broker e recebe uma nova mensagem
def on_connect(client, userdata, flags, rc):
    # Caso nao ocorrer nenhum erro exibe a mensagem de Connected
    print("Connected!", str(rc))

    # Apos conectado no servidor registra o(s) topicos(s) para subscribe
    client.subscribe(mqtt_topic)


# Funcao responsavel em decodificar uma mensagem quando recebida
def on_message(client, userdata, msg):

    # Obtem os dados vindos do Broker/MQTT
    newTopic = msg.topic.split("/", 1)
    msg.payload = msg.payload.decode("utf-8")

    # Obtem do Banco o Id do respectivo sensor
    sensor = selectSensorNick(connection, newTopic[1])

    # A partir dos dados obtidos anteriormente, armazena as informacoes na respectiva tabela
    weatherData = WeatherData(int(999), sensor.id, msg.payload)
    insertWeatherData(connection, weatherData)
    updateRowDefaultConf(connection, weatherData)

    print("\n")
    print("MQTT Data Received...")
    print("MQTT Topic: " + newTopic[0])
    print("MQTT Sensor: " + newTopic[1])
    print("Data: " + str(msg.payload))
    print("\n")


# The message itself is stored in the msg variable
# and details about who sent it are stored in userdata

# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client.on_connect = on_connect
client.on_message = on_message

# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(mqtt_broker_ip, mqtt_broker_port)

# Once we have told the client to connect, let the client object run itself
client.loop_forever()
client.disconnect()
