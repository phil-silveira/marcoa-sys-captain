"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 23/12/2019

Aplicacao que possui toda a logica de funcionamento da aplicacao Web DJANGO. Extrai todas
as informacoes necessarios dos MODELS e renderiza as mesmas em template conforme os arquivos
contidos na pasta templates. Sao as funcoes que recebem requisicoes web e retornam uma resposta
web.
"""
from collections import namedtuple

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.db import connection
from django.template.loader import render_to_string
from .forms import *

from .static.libs.publish import publish_To_Topic

## VARIAVEIS GLOBAIS
vStatus = int(0)
vProgTemp = int(0)
vTemp = int(0)
vEnvTemp = int(0)
vTempRows = int(0)


# Seleciona os dados referente as configuracoes padroes de uma linha
def selectRowDefaultConf(row):
    row = get_object_or_404(RowDefaultConf, row=row)
    return row

# Funcao que tem por objetivo retornar um conjunto de objetos que
# sao acessiveis por nome de campos ou indices
# https://docs.djangoproject.com/pt-br/2.2/topics/db/sql/#executing-custom-sql-directly
def namedtuplefetchall(cursor):
	desc = cursor.description
	nt_result = namedtuple('Result', [col[0] for col in desc])
	return [nt_result(*row) for row in cursor.fetchall()]

# Metodo responsavel em obter todas as listas cadastradas no banco
# e enviar esse conjunto de dados para o arquivo rows_list.html
# para que estes possam ser renderizados
@login_required
def row_list(request, template_name="rows_list.html"):
    row = Row.objects.order_by('id')
    rows = {'list': row}
    return render(request, template_name, rows)


# Metodo responsavel em obter todas as listas cadastradas no banco
# e enviar esse conjunto de dados para o arquivo rows_list_qc.html
# para que estes possam ser renderizados no formato de tabela
@login_required
def row_list_qc(request, template_name="rows_list_qc.html"):
    row = Row.objects.order_by('id')
    rows = {'list': row}
    return render(request, template_name, rows)


# Metodo responsavel em obter as configuracoes do sistema
# e rendereizar as mesmas para a pagina de configuracoes
@login_required
def configurations(request, template_name="configurations.html"):
    farmProperty = FarmProperty.objects.order_by('id')

    personGer = Person.objects.filter(group_id=1)
    personTec = Person.objects.filter(group_id=2)
    personOpe = Person.objects.filter(group_id=3)

    context = {
        'farmProperty': farmProperty,
        'personGer': personGer,
        'personTec': personTec,
        'personOpe': personOpe}

    return render(request, template_name, context)


# Metodo responsavel em obter criar a pagina SOBRE
# e rendereizar as mesmas para a pagina de configuracoes
@login_required
def about(request, template_name="about.html"):

    return render(request, template_name)


# Metodo responsavel em realizar todos os procedimentos
# para relatórios e apos renderizar os resultados na pagina
# reports.html
@login_required
def reports(request, template_name="reports.html"):
    return render(request, template_name)


# Funcao que renderiza o dados de uma linha a partir da
# sua chave primario
@login_required
def row_details(request, pk, template_name="row_details.html"):
    global vStatus
    global vProgTemp
    global vTemp
    global vEnvTemp

    row = get_object_or_404(Row, pk=pk)

    values = get_lastWeatherDataPerRowAndSensor(pk)
    valueStatus = int(values[0].status)
    valueTemp = int(values[0].temp)
    valueProgTemp = int(values[0].progtemp)
    valueEnvTemp = int(values[0].envtemp)

    context = {
        'row': row,
        'valueStatus': valueStatus,
        'valueProgTemp': valueProgTemp,
        'valueTemp': valueTemp,
        'valueEnvTemp': valueEnvTemp
    }

    return render(request, template_name, context)

# Funcao utilizada pela API que retorna um conjunto de dados meteorologicos
# a partir do identtificador da linha e identificador do sensor
@login_required
def get_weatherData(request, row_id, sensor_id):
    weatherData = WeatherData.objects.filter(row_id=row_id, sensor_id=sensor_id)
    date = [obj.read_date for obj in weatherData]
    value = [float(obj.value) for obj in weatherData]

    context = {
        "date": date,
        "value": value,
    }
    return JsonResponse(context)

# Funcao utilizada pela API que retorna um conjunto de dados meteorologicos
# a partir do sensor e todas as linhas das ultimas 24 horas
@login_required
def get_weatherDataAllPerSensor(request, sensor_id):
    simpleList = []
    #row = Row.objects.order_by('id')
    row = Row.objects.filter(id__lt=999).order_by('id')
    #print(row)
    for x in range(len(row)):
        with connection.cursor() as cursor:
            r = int(x + 1)
            #print(r)
            if sensor_id != 10:
                cursor.execute("select * from app_weatherdata where read_date > now() - interval '1 hours' and row_id=%s and sensor_id=%s order by read_date",(r, sensor_id,))
            else:
                cursor.execute("select * from app_weatherdata where read_date > now() - interval '30 days' and row_id=%s and sensor_id=%s order by read_date",(r, sensor_id,))

            w = namedtuplefetchall(cursor)
            #print(w)

            date = [obj.read_date for obj in w]
            value = [float(obj.value) for obj in w]

            context = {
                "date": date,
                "value": value,
            }

            simpleList.append(context)

    return JsonResponse(simpleList, safe=False)

# Funcao utilizada pela API que retorna um conjunto de dados meteorologicos
# a partir da linha e os sensores de temperatura observada, ambiente e programada
# das ultimas 24 horas
@login_required
def get_weatherDataTempsPerRow(request, row_id):
    simpleList = []
    sensorList = [1, 8, 9]
    for x in range(0, len(sensorList)):
        with connection.cursor() as cursor:
            cursor.execute(
                "select * from app_weatherdata where read_date > now() - interval '1 hours' and row_id=%s and sensor_id=%s order by read_date",(row_id, sensorList[x],))

            w = namedtuplefetchall(cursor)

            date = [obj.read_date for obj in w]
            value = [float(obj.value) for obj in w]

            context = {
                "date": date,
                "value": value,
            }
            simpleList.append(context)

    return JsonResponse(simpleList, safe=False)


# Funcao utilizada pela API que retorna um conjunto de dados meteorologicos
# a partir da linha e o sensor de consumo das ultimas 24 horas
@login_required
def get_weatherDataConsumPerRow(request, row_id):
    simpleList = []
    sensorList = [7]
    for x in range(0, len(sensorList)):
        with connection.cursor() as cursor:
            cursor.execute(
                "select * from app_weatherdata where read_date > now() - interval '1 hours' and row_id=%s and sensor_id=%s order by read_date",(row_id, sensorList[x],))

            w = namedtuplefetchall(cursor)

            date = [obj.read_date for obj in w]
            value = [float(obj.value) for obj in w]

            context = {
                "date": date,
                "value": value,
            }
            simpleList.append(context)

    return JsonResponse(simpleList, safe=False)

# Funcao utilizada pela API que retorna um conjunto de dados meteorologicos
# a partir da linha e o sensor da Media do consumo dos ultimos 30 dias
@login_required
def get_weatherdataAvgDailyConsumPerRow(request, row_id):
    simpleList = []
    sensorList = [10]
    for x in range(0, len(sensorList)):
        with connection.cursor() as cursor:
            cursor.execute(
                "select * from app_weatherdata where read_date > now() - interval '30 days' and row_id=%s and sensor_id=%s ",(row_id, sensorList[x],))

            w = namedtuplefetchall(cursor)

            date = [obj.read_date for obj in w]
            value = [float(obj.value) for obj in w]

            context = {
                "date": date,
                "value": value,
            }
            simpleList.append(context)

    return JsonResponse(simpleList, safe=False)

# Funcao utilizada pela API que retorna o conjunto dos ultimos dados recebidos via MQTTT
# Passando por parametro o respectivo sensor para cada linha
# Adiciona todos os dados em uma lista e devolve para a API
# https://docs.djangoproject.com/pt-br/2.2/topics/db/sql/#executing-custom-sql-directly
@login_required
def get_lastWeatherDataPerSensorAndRow(request, sensor_id):
    simpleList = []
    row = Row.objects.order_by('id')
    for x in range(len(row)):
        with connection.cursor() as cursor:
            r = int(x + 1)
            cursor.execute(
                "select * from app_weatherdata where ((select max(id) from app_weatherdata where row_id=%s and sensor_id=%s)=id)", (r, sensor_id,))

            w = namedtuplefetchall(cursor)

            row = [obj.row_id for obj in w]
            read_date = [obj.read_date for obj in w]
            value = [float(obj.value) for obj in w]

            context = {
                "row": row,
                "read_date": read_date,
                "value": value,
            }
            simpleList.append(context)

    return JsonResponse(simpleList, safe=False)

# Funcao utilizada pela API que retorna o conjunto dos ultimos dados recebidos via MQTTT
# Passando por parametro o respectivo sensor e linha
# https://docs.djangoproject.com/pt-br/2.2/topics/db/sql/#executing-custom-sql-directly
def get_lastWeatherDataPerRowAndSensor(row_id):
    with connection.cursor() as cursor:
        cursor.execute("select * from app_rowdefaultconf where row_id=%s", (row_id,))
        #cursor.execute("SELECT * FROM app_weatherdata WHERE (row_id, read_date) IN (SELECT row_id, Max(read_date) FROM app_weatherdata GROUP BY row_id) and row_id=%s and sensor_id=%s ORDER BY sensor_id ASC", (row_id, sensor_id,))

        weatherDatas = namedtuplefetchall(cursor)

    return weatherDatas

# Funcao que tem por objetivo logar no sistema
# Obtem os dados vindos do formulario e tenta realizar o login
# Caso satisfatorio encaminha o usuario para a tela que lista todas
# as linhas do sistema, caso contrario reencaminha para a tela de login
# novamente.
def logar(request, template_name="login.html"):
    next = request.GET.get('next', '/rows/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next)

        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, template_name, {'redirect_to': next})


# Funcao que tem por objetivo deslogar o usuario do sistema
# A funcao logout e nativa do django e realiza todas as
# tarefas necessarias para deslogar o usuario
def deslogar(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


def save_ajust_temp_new(request, pk, form, template_name):

    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            fs = form.save(commit=False)
            fs.user = request.user
            fs.row = pk
            fs.save()
            MQTT_Topic_AjustTemp = "qc1/row" + str(pk) + "/ajustprogtemp"
            AjustTemp_Fake_Value = float("{0:.1f}".format(fs.value))
            publish_To_Topic(MQTT_Topic_AjustTemp, AjustTemp_Fake_Value)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form, 'row': pk}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def ajust_temp_new(request, pk):
    if request.method == 'POST':
        form = AjustTempNewForm(request.POST)
    else:
        form = AjustTempNewForm()
    return save_ajust_temp_new(request, pk, form, 'partial_ajust_temp_new.html')


def save_ajust_status_new(request, pk, form, template_name):
    #from .static.libs.publish import publish_To_Topic
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            fs = form.save(commit=False)
            fs.user = request.user
            fs.row = pk
            fs.save()

            row = selectRowDefaultConf(pk)
            MQTT_Topic_AjustTemp = "qc1/row" + str(pk) + "/ajustprogtemp"
            AjustTemp_Fake_Value = float("{0:.1f}".format(row.progtemp))
            publish_To_Topic(MQTT_Topic_AjustTemp, AjustTemp_Fake_Value)


            MQTT_Topic_AjustStatus = "qc1/row" + str(pk) + "/ajuststatus"
            AjustStatus_Fake_Value = fs.status
            publish_To_Topic(MQTT_Topic_AjustStatus, AjustStatus_Fake_Value)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form, 'row': pk}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def ajust_status_new(request, pk):
    if request.method == 'POST':
        form = AjustStatusNewForm(request.POST)
    else:
        form = AjustStatusNewForm()
    return save_ajust_status_new(request, pk, form, 'partial_ajust_status_new.html')