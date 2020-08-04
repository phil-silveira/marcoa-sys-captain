"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 23/12/2019

Aplicacao que possui a declaracao dos forms utilizados pela pagina Web DJANGO
"""
from django import forms

from .models import *

class AjustTempNewForm(forms.ModelForm):

    class Meta:
        model = AjustTempNew
        fields = ('value',)
        labels = {"value": "Valor"}

class AjustStatusNewForm(forms.ModelForm):

    class Meta:
        model = AjustStatusNew
        fields = ('status',)
        labels = {"status": "Status"}