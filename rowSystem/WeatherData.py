"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 23/12/2019

Classe que armazena os  respectivos atributos referente aos dados dos sensores
"""
class WeatherData:
    def __init__(self, row, sensor, value):
        self.row = row
        self.sensor = sensor
        self.value = value

    def setRow(self, row):
        self.row = row

    def setSensor(self, sensor):
        self.sensor = sensor

    def setValue(self, value):
        self.value = value

    def getRow(self):
        return self.row

    def getSensor(self):
        return self.sensor

    def getValue(self):
        return self.value

