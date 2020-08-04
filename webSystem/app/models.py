"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 23/12/2019

Aplicacao que tem por objetivo descrever as classes/modelos utilizados pela aplicacao Web DJANGO.
Estas se referem as tabelas utilizadas no banco de dados Postgres SQL
"""
from django.conf import settings
from django.db import models
from .validators import validate_value_ajust_temp


############################################################################################################
# Classe que descreve o sensor
class Sensor(models.Model):
    description = models.CharField(max_length=45, null=False)
    nick = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.description
############################################################################################################





############################################################################################################
# Classe que descreve o Pavilião
class Pavilion(models.Model):
    description = models.CharField(max_length=45, null=False)
    nick = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.description
############################################################################################################





############################################################################################################
# Classe que descreve o Grupo da Pessoa (Gerente ou Operador)
class Person_Group(models.Model):
    description = models.CharField(max_length=45, null=False)

    def __str__(self):
        return self.description
############################################################################################################




############################################################################################################
# Classe que descreve o Grupo da Pessoa (Gerente ou Operador)
class FarmProperty(models.Model):
    TYPE_DOC_CHOICES = (
        ("cnpj", "CNPJ"),
        ("cpf", "CPF")
    )
    description = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=45, null=False)
    city = models.CharField(max_length=45, null=False)
    state = models.CharField(max_length=45, null=False)
    email = models.CharField(max_length=45, null=False)
    phone = models.CharField(max_length=45, null=False)
    type_doc = models.CharField(max_length=45, null=False, choices=TYPE_DOC_CHOICES)
    num_doc = models.CharField(max_length=45, null=False, blank=False)

    def __str__(self):
        return self.description
############################################################################################################





############################################################################################################
class Person(models.Model):
    TYPE_DOC_CHOICES = (
        ("cnpj", "CNPJ"),
        ("cpf", "CPF")
    )
    name = models.CharField(max_length=45, null=False)
    email = models.CharField(max_length=45, null=True)
    phone = models.CharField(max_length=45, null=False)
    group = models.ForeignKey(Person_Group, on_delete=models.CASCADE)
    farm = models.ForeignKey(FarmProperty, on_delete=models.CASCADE)
    type_doc = models.CharField(max_length=45, null=False, choices=TYPE_DOC_CHOICES)
    num_doc = models.CharField(max_length=45, null=False, blank=False)

    def __str__(self):
        return str(self.name) + " " + str(self.email) + " " + str(self.phone) + " " + str(self.farm)
############################################################################################################





############################################################################################################
# Classe que descreve as variaveis que serao utilizadas no sistema
# Por exemplo, temperatura
class ControlBoard(models.Model):
    description = models.CharField(max_length=45, null=False)
    nick = models.CharField(max_length=45, null=True)
    pavilion = models.OneToOneField(Pavilion, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
############################################################################################################






############################################################################################################
# Classe que descreve as variaveis que serao utilizadas no sistema
# Por exemplo, temperatura
class Row(models.Model):
    INATIVA = 0
    ATIVA = 1

    TYPE_DOC_CHOICES = (
        (ATIVA, "Ativa"),
        (INATIVA, "Inativa")
    )
    description = models.CharField(max_length=45, null=False)
    nick = models.CharField(max_length=45, null=True)
    state = models.PositiveSmallIntegerField(choices=TYPE_DOC_CHOICES, default=0)
    controlBoard = models.ForeignKey(ControlBoard, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
############################################################################################################




############################################################################################################
class WeatherData(models.Model):
    read_date = models.DateTimeField(auto_now_add=True, verbose_name="Data da leitura")
    row = models.ForeignKey(Row, null=True, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, null=True, on_delete=models.CASCADE)
    value = models.FloatField(null=False)

    def __str__(self):
        return str(self.read_date) + " " + str(self.row) + " " + str(self.sensor) + " " + str(self.value)
############################################################################################################



############################################################################################################
class AjustTempNew(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name="Data do registro")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    row = models.IntegerField(null=True )
    value = models.FloatField(null=False, validators=[validate_value_ajust_temp])

    def __str__(self):
        return str(self.date) + " " + str(self.user) + " " + str(self.row) + " " + str(self.value)
############################################################################################################


############################################################################################################
class AjustStatusNew(models.Model):

    DESLIGAR = 0
    LIGAR = 1

    TYPE_DOC_CHOICES = (
        (LIGAR, "Ligar"),
        (DESLIGAR, "Desligar")
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Data do registro")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    row = models.IntegerField(null=True )
    status = models.PositiveSmallIntegerField(choices=TYPE_DOC_CHOICES)

    def __str__(self):
        return str(self.date) + " " + str(self.user) + " " + str(self.row) + " " + str(self.status)
############################################################################################################

############################################################################################################
class RowDefaultConf(models.Model):
    DESLIGADA = 0
    LIGADA = 1

    TYPE_DOC_CHOICES = (
        (LIGADA, "Ligada"),
        (DESLIGADA, "Desligada")
    )
    row = models.OneToOneField(Row, null=False, blank=False, on_delete=models.CASCADE)
    temp = models.FloatField(null=True)
    progtemp = models.FloatField(null=True)
    envtemp = models.FloatField(null=True)
    status = models.PositiveSmallIntegerField(choices=TYPE_DOC_CHOICES)

    def __str__(self):
        return str(self.row) + " " + str(self.temp) + " " + str(self.progtemp) + " " + str(self.envtemp) + " " + str(self.status)
############################################################################################################