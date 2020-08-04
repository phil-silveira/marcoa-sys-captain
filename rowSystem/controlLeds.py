"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 19/11/2019

Funcao que tem por objetivo controlar os leds do quadro de comando. Ativando ou desativando os leds
das respectivas linhas
"""
import RPi.GPIO as GPIO
import time
from sys import argv

# Define o status do ambiente
def setEnvStatus(envenvironment, status):
    row1 = 17
    row2 = 18
    row3 = 22
    row4 = 23
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(row1, GPIO.OUT)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(row2, GPIO.OUT)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(row3, GPIO.OUT)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(row4, GPIO.OUT)
    if status=="off":
        if envenvironment=="row1":
            GPIO.output(row1, False)
        if envenvironment=="row2":
            GPIO.output(row2, False)
        if envenvironment=="row3":
            GPIO.output(row3, False)
        if envenvironment=="row4":
            GPIO.output(row4, False)
        if envenvironment=="all":
            GPIO.output(row1, False)
            GPIO.output(row2, False)
            GPIO.output(row3, False)
            GPIO.output(row4, False)
    if status=="on":
        if envenvironment=="row1":
            GPIO.output(row1, True)
        if envenvironment=="row2":
            GPIO.output(row2, True)
        if envenvironment=="row3":
            GPIO.output(row3, True)
        if envenvironment=="row4":
            GPIO.output(row4, True)
        if envenvironment=="all":
            GPIO.output(row1, True)
            GPIO.output(row2, True)
            GPIO.output(row3, True)
            GPIO.output(row4, True)
