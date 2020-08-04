"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 23/12/2019
Versao: 1.2

Aplicacao responsavel por realizar diversas operacoes do banco de dado
conforme documentacao inicial em cada funcao
"""

from datetime import datetime, date
import psycopg2 as pdb
import psycopg2.extras
from Row import Row
from RowDefaultConf import RowDefaultConf
from Sensor import Sensor

# Insere valores dos dados conforme o ambiente e sensor
def insertWeatherData(connection, weatherData):
    try:
        with connection:

            cur = connection.cursor()

            data_e_hora_em_texto = "{:%d-%m-%Y %H:%M:%S}".format(datetime.now())
            data_e_hora = datetime.strptime(data_e_hora_em_texto, '%d-%m-%Y %H:%M:%S')

            value = "{:.1f}".format(float(weatherData.getValue()))

            cur.execute("INSERT INTO app_weatherdata (read_date, value, row_id, sensor_id) VALUES (%s,%s,%s,%s)",
                        (data_e_hora, value, weatherData.getRow(), weatherData.getSensor()))
            count = cur.rowcount
            print(count, "Record inserted successfully into table app_weatherdata")
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("failed to insert into table Weatherdata", error)


# Seleciona os dados referente a uma linha pelo nick
def selectRowNick(connection, nick):
    try:
        with connection:
            cur = connection.cursor(cursor_factory=pdb.extras.DictCursor)
            cur.execute("SELECT * FROM app_row where nick = %s", (nick, ))
            records = cur.fetchone()
            row = Row()
            row.setId(records[0])
            row.setDescription(records[1])
            row.setAddressIP(records[2])
            row.setControlBoard(records[3])
            row.setNick(records[4])
            return row


    except (Exception, pdb.Error) as error:
        print("Failed to select Row nickname", error)


# Seleciona os dados referente a um sensor pelo nick
def selectSensorNick(connection, nick):
    try:
        with connection:
            cur = connection.cursor(cursor_factory=pdb.extras.DictCursor)
            cur.execute("SELECT * FROM app_sensor where nick=%s", (nick, ))
            records = cur.fetchone()
            sensor = Sensor()
            sensor.setId(records[0])
            sensor.setDescription(records[1])
            sensor.setNick(records[2])
            return sensor


    except (Exception, pdb.Error) as error:
        print("Failed to select Sensor nickname", error, nick)


# Seleciona o id de uma linha
def selectIdRow(connection):
    try:
        with connection:
            cur = connection.cursor(cursor_factory=pdb.extras.DictCursor)
            cur.execute("SELECT id FROM app_row")
            records = cur.fetchall()
            return records


    except (Exception, pdb.Error) as error:
        print("Failed to select Row Id", error)


# Seleciona a média diária de consumo de cada linha
def selectAvgDalyConsum(connection, row):
    try:
        with connection:
            cur = connection.cursor(cursor_factory=pdb.extras.DictCursor)
            cur.execute("select avg(value) from app_weatherdata where row_id=%s and sensor_id=7 and read_date::date=%s::timestamp::date", (row, datetime.now().strftime('%Y-%m-%d')))
            records = cur.fetchall()
            return records


    except (Exception, pdb.Error) as error:
        print("Failed to select Avg Daly Consum", error)


# Seleciona o tempo total em que o sistema ficou Online
def selectSysUp(connection, row):
    try:
        with connection:
            cur = connection.cursor(cursor_factory=pdb.extras.DictCursor)
            cur.execute("select count(*) from app_weatherdata where row_id=%s and sensor_id=3 and value=1 and read_date::date=%s::timestamp::date", (row, datetime.now().strftime('%Y-%m-%d')))
            records = cur.fetchall()
            return records


    except (Exception, pdb.Error) as error:
        print("Failed to select Sys Up", error)


# Seleciona os dados referente as configuracoes padroes de uma linha
def selectRowDefaultConf(connection, row):
    try:
        with connection:
            cur = connection.cursor(cursor_factory=pdb.extras.DictCursor)
            cur.execute("SELECT * FROM app_rowdefaultconf where row_id=%s", (row, ))
            records = cur.fetchone()
            #print("DADOS VINDOS DO BANCO=======>" + str(records))
            rowDefaultConf = RowDefaultConf()
            rowDefaultConf.setId(records[0])
            rowDefaultConf.setProgTemp(records[1])
            rowDefaultConf.setStatus(records[2])
            rowDefaultConf.setRowId(records[3])
            return rowDefaultConf


    except (Exception, pdb.Error) as error:
        print("Failed to select Row Configuration", error)


# A partir do id do sensor atualiza a tabela referente a ultima configuracao valida de uma linha
def updateRowDefaultConf(connection, weatherData):
    try:
        with connection:
            cur = connection.cursor(cursor_factory=pdb.extras.DictCursor)
            if weatherData.getSensor() == 1:
                cur.execute("UPDATE app_rowdefaultconf SET temp=%s WHERE row_id=%s", (weatherData.getValue(), weatherData.getRow(),))
            elif weatherData.getSensor() == 3:
                cur.execute("UPDATE app_rowdefaultconf SET status=%s WHERE row_id=%s", (weatherData.getValue(), weatherData.getRow(),))
            elif weatherData.getSensor() == 8:
                cur.execute("UPDATE app_rowdefaultconf SET progtemp=%s WHERE row_id=%s", (weatherData.getValue(), weatherData.getRow(),))
            elif weatherData.getSensor() == 9:
                cur.execute("UPDATE app_rowdefaultconf SET envtemp=%s WHERE row_id=1", (weatherData.getValue(),))

            connection.commit()
            print("Number of rows updated:", cur.rowcount)
            if cur.rowcount == 0:
                print("Record Not Updated !!!")


    except (Exception, pdb.Error) as error:
        print("Failed to select Row Default Configuration", error)
