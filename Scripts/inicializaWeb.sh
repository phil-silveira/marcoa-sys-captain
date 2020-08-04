#!/bin/bash

# Autor: GKW Agro Tech
# Titulares: 
# 	GKW Agro Tech
# 	MarcoA Instalacao de Sistemas de Aquecimento Ltda	
# Create Date: 11/11/2019
# Update Date: 19/11/2019
# Versao: 1.1
#
# Aplicacao responsavel por iniciar o servico web na porta TCP 8000

echo -e "Entrando no diretorio"
source /home/pi/MarcoA/webSystem/bin/activate
echo -e "Ativando..."
python3 /home/pi/MarcoA/webSystem/manage.py runserver 0.0.0.0:8000 > /home/pi/MarcoA/logSystem/webSystem.log 2>&1
echo -e "Servico iniciado..." 
