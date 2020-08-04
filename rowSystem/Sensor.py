"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 19/11/2019

Classe que possui os principais atributos referente a um sensor
"""
class Sensor:
    def __init__(self, description,  nick):
        self.description = description
        self.nick = nick

    def __init__(self):
        pass

    def setId(self, id):
        self.id = id

    def setDescription(self, description):
        self.description = description

    def setNick(self, nick):
        self.nick = nick

    def getId(self):
        return self.id

    def getDescription(self):
        return self.description

    def getNick(self):
        return self.nick