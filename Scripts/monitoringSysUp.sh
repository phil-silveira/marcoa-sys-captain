#!/usr/bin/env bash

# Autor: GKW Agro Tech
# Titulares: 
# 	GKW Agro Tech
# 	MarcoA Instalacao de Sistemas de Aquecimento Ltda	
# Create Date: 11/11/2019
# Update Date: 19/11/2019
# Versao: 1.1
#
# Aplicacao responsavel por iniciar o servico que ira ser executado
# diariamente para obter o tempo em que o sistema das linhas ficaram 
# ligados

echo -e "Entrando no diretorio"
sleep 2
source /home/pi/MarcoA/rowSystem/bin/activate
echo -e "Ativando..."
sleep 2
python3 /home/pi/MarcoA/rowSystem/sysup.py > /home/pi/MarcoA/logSystem/monitoringSysUp.log 2>&1
echo -e "Servico iniciado..." 
sleep 3
