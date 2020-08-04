#!/bin/bash

# Autor: GKW Agro Tech
# Titulares: 
# 	GKW Agro Tech
# 	MarcoA Instalacao de Sistemas de Aquecimento Ltda	
# Create Date: 11/11/2019
# Update Date: 19/11/2019
# Versao: 1.1
#
# Aplicacao responsavel por iniciar os serviços NGROK para acesso remoto

/home/pi/MarcoA/Scripts/ngrok http -config=/home/pi/.ngrok2/ngrok.yml -subdomain=app.us 8000 > /dev/null &
/home/pi/MarcoA/Scripts/ngrok tcp -config=/home/pi/.ngrok2/ngrok.yml --region=sa --remote-addr 1.tcp.sa.ngrok.io:20304 22 > /dev/null &
/home/pi/MarcoA/Scripts/ngrok tcp -config=/home/pi/.ngrok2/ngrok.yml --region=sa --remote-addr 1.tcp.sa.ngrok.io:20468 5900 > /dev/null &
