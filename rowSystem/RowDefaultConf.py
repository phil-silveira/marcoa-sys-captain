"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 23/12/2019

Classe que possui os principais atributos da configuracao inicial de uma ambiente
"""

class RowDefaultConf:
    def __init__(self):
        pass

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def setRowId(self, rowid):
        self.rowid = rowid

    def setProgTemp(self, progtemp):
        self.progtemp = progtemp

    def getRowId(self):
        return self.rowid

    def getProgTemp(self):
        return self.progtemp

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status