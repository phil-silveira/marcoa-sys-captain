"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 19/11/2019

Aplicacao que tem por objetivo realizar a conexao com o servidor MQTT e publicar uma informacao nessa rede
Esta aplicacao eh instanciada pelo script bash do quadro de comando
"""

import time
from publish import publish_To_Topic
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

while True:
    temperature = sensor.get_temperature()
    MQTT_Topic_AjustTemp = "qc1/envtemp"
    AjustTemp_Fake_Value = float("{0:.1f}".format(temperature))
    publish_To_Topic(MQTT_Topic_AjustTemp, AjustTemp_Fake_Value)
    print("The temperature is %s ˚C" % temperature)
    time.sleep(60)
