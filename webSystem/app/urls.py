"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 23/12/2019

Aplicacao que possui as URLs utilizadas pela aplicacao Web DJANGO.
"""
from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('logar/', logar, name='logar'),
    path('deslogar/', deslogar, name='deslogar'),
    path('rows/', row_list, name='row_list'),
    path('rows_qc/', row_list_qc, name='row_list_qc'),
    path('configurations/', configurations, name='configurations'),
    path('reports/', reports, name='reports'),
    path('about/', about, name='about'),
    path('api/weatherData/getAll/<int:row_id>/<int:sensor_id>/', get_weatherData, name='get-weatherdata'),
    path('api/weatherData/getAll/<int:sensor_id>/', get_weatherDataAllPerSensor, name='get-weatherdataAllPerSensor'),
    path('api/weatherData/getTempsPerRow/<int:row_id>/', get_weatherDataTempsPerRow, name='get-weatherdataTempsPerRow'),
    path('api/weatherData/getConsumPerRow/<int:row_id>/', get_weatherDataConsumPerRow, name='get-weatherdataConsumPerRow'),
    path('api/weatherData/getAvgDailyConsumPerRow/<int:row_id>/', get_weatherdataAvgDailyConsumPerRow, name='get-weatherdataAvgDailyConsumPerRow'),
    path('api/weatherData/getSensor/<int:sensor_id>/', get_lastWeatherDataPerSensorAndRow, name='get-weatherdata-temp'),
    path('row/details/<int:pk>/', row_details, name='row_details'),
    path('ajust/<int:pk>/', ajust_temp_new, name='ajust_temp_new'),
    path('ajuststatus/<int:pk>/', ajust_status_new, name='ajust_status_new')
]