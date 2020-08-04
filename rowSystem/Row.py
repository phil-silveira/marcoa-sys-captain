"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 19/11/2019

Classe de uma ambiente, possui os respectivos atributos
"""

class Row:
    def __init__(self, description, addressIP, controlBoard, nick):
        self.description = description
        self.addressIP = addressIP
        self.controlBoard = controlBoard
        self.nick = nick

    def __init__(self):
        pass

    def setId(self, id):
        self.id = id

    def setDescription(self, description):
        self.description = description

    def setAddressIP(self, addressIP):
        self.addressIP = addressIP

    def setControlBoard(self, controlBoard):
        self.controlBoard = controlBoard

    def setNick(self, nick):
        self.nick = nick

    def getId(self):
        return self.id

    def getDescription(self):
        return self.description

    def getAddressIP(self):
        return self.addressIP

    def getControlBoard(self):
        return self.controlBoard

    def getNick(self):
        return self.nick