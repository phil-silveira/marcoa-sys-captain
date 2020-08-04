"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 19/11/2019
Versao: 1.1

Aplicacao que tem por objetivo validar um determinado campo de um formulario da
aplicacao Web DJANGO
"""
from django.core.exceptions import ValidationError

# http://www.learningaboutelectronics.com/Articles/How-to-create-a-custom-field-validator-in-Django.php
def validate_value_ajust_temp(value):
    if value > 37 or value < 27:
        raise ValidationError("Temperatura requerida está abaixo ou acima da permitida !!!")
    else:
        return value