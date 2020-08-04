"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 19/11/2019

Funcao que tem por objetivo obter todas as linhas cadastradas
obter o tempo em que uma linha ficou online, apos armazena as
respectivas informacoes no banco de dados
"""

from db_config import connection
from db_store import *
from WeatherData import WeatherData

ids = selectIdRow(connection)
for i in range(len(ids)):
    linha = int(ids[i][0])
    sysup = selectSysUp(connection, linha)

    if sysup[0][0] is not None:
        c = sysup[0][0]
        c = int(c/720)
        if c < 1:
            c = 1
        # A partir dos dados obtidos anteriormente, armazena as informacoes na respectiva tabela
        weatherData = WeatherData(linha, int(11), c)
        insertWeatherData(connection, weatherData)

        #print("Linha: " + str(linha) + " Tempo Ligada: " + str(c) + " horas")