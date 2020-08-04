#!/usr/bin/env bash

# Autor: GKW Agro Tech
# Titulares: 
# 	GKW Agro Tech
# 	MarcoA Instalacao de Sistemas de Aquecimento Ltda	
# Create Date: 11/11/2019
# Update Date: 19/11/2019
# Versao: 1.1
#
# Aplicacao responsavel por iniciar o servico que chama o servico para
# ler uma determinada variavel na rede MQTT do quadro de comando

echo -e "Entrando no diretorio"
sleep 2
source /home/pi/MarcoA/rowSystem/bin/activate
echo -e "Ativando..."
sleep 2
python3 /home/pi/MarcoA/rowSystem/subscribe_qc1.py > /home/pi/MarcoA/logSystem/qcSystemSub_1.log 2>&1
echo -e "Servico iniciado..."
sleep 3
