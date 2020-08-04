"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 23/12/2019

Aplicacao que tem por objetivo obter todas as linhas cadastradas
obter a media de consumo diaria e armazenar a mesma em uma nova
variavel no banco de dados
"""

from db_config import connection
from db_store import *
from WeatherData import WeatherData

ids = selectIdRow(connection)
for i in range(len(ids)):
    linha = int(ids[i][0])
    consum = selectAvgDalyConsum(connection, linha)

    if consum[0][0] is not None:
        c = consum[0][0]
        # A partir dos dados obtidos anteriormente, armazena as informacoes na respectiva tabela
        weatherData = WeatherData(linha, int(10), c)
        insertWeatherData(connection, weatherData)

        # print("Linha: " + str(linha) + " CONSUMO: " + str(c))