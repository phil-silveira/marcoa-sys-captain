"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 23/12/2019

Aplicacao responsavel por ler os dados oriundos do ambiente 5
a partir de uma rede MQTT. Recebe essas informacoes, interpreta
e armazena a partir do tipo do sensor o respectivo dado no banco
de dados
"""
import paho.mqtt.client as mqtt
from db_config import connection
from db_store import *
from WeatherData import WeatherData
from publish import publish_To_Topic
from controlLeds import setEnvStatus

# Assinando o TOPIC e definindo o Broker e sua Respectiva porta
environment = "row5"
qc = "qc1"
mqtt_topic = environment + "/#"
#mqtt_broker_ip = "192.168.0.12"
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

    if newTopic[1] == "rowwantcall":
        # Obtem do Banco o Id da respectiva linha
        row = selectRowNick(connection, newTopic[0])
        rowDefaultConf = selectRowDefaultConf(connection, row.getId())

        MQTT_Topic_AjustTemp = qc + "/" + environment + "/ajustprogtemp"
        AjustTemp_Fake_Value = float("{0:.1f}".format(rowDefaultConf.getProgTemp()))
        publish_To_Topic(MQTT_Topic_AjustTemp, AjustTemp_Fake_Value)

        MQTT_Topic_AjustStatus = qc + "/" + environment + "/ajuststatus"
        AjustStatus_Fake_Value = rowDefaultConf.getStatus()
        publish_To_Topic(MQTT_Topic_AjustStatus, AjustStatus_Fake_Value)

    else:

        # Obtem do Banco o Id da respectiva linha
        row = selectRowNick(connection, newTopic[0])

        # Obtem do Banco o Id do respectivo sensor
        sensor = selectSensorNick(connection, newTopic[1])

        # A partir dos dados obtidos anteriormente, armazena as informacoes na respectiva tabela
        weatherData = WeatherData(row.id, sensor.id, msg.payload)
        insertWeatherData(connection, weatherData)
        updateRowDefaultConf(connection, weatherData)

        print("\n")
        print("MQTT Data Received...")
        print("MQTT Topic: " + newTopic[0])
        print("MQTT Sensor: " + newTopic[1])
        print("Data: " + str(msg.payload))
        print("\n")

        if sensor.id == 3:
            if int(weatherData.getValue()) == 0:
                setEnvStatus(environment, "off")
            else:
                setEnvStatus(environment, "on")

        if sensor.id == 2:
            # Valor referente do dimmer lido em cada linha/ambiente
            value = "{:.1f}".format(float(weatherData.getValue()))

            # Realiza uma regra de 3 para verificar o valor correspondente
            # em volts (aproximadamente)
            volts = (float(float(value)) * 220) / 95
            # Sensor correspondente ao tensao eletrica
            s_volts = 4
            # Cria o WeatherData e armazena no banco
            wd_volts = WeatherData(row.id, s_volts, volts)
            insertWeatherData(connection, wd_volts)

            # Valor de amperagem dos cabos
            amps = (float(float(value)) * 1.6) / 95
            # Sensor correspondente ao corrente eletrica
            s_amps = 5
            # Cria o WeatherData e armazena no banco
            wd_amps = WeatherData(row.id, s_amps, amps)
            insertWeatherData(connection, wd_amps)

        # Calculo do consumo em watts
        watts = float(volts * amps)
        # Sensor correspondente ao consumo
        s = 7
        # Cria o WeatherData e armazena no banco
        wd = WeatherData(row.id, s, watts)
        insertWeatherData(connection, wd)


# Apos receber uma conexxao, chama  a funcao para interpretar a mensagem
client.on_connect = on_connect
client.on_message = on_message

# Conecta a uma rede MQTT a partir do IP e Porta do Broker/Server MQTT
client.connect(mqtt_broker_ip, mqtt_broker_port)

# Apos realizar as tarefas de armazenamento, desconecta do Broker/Server MQTT
client.loop_forever()
client.disconnect()
