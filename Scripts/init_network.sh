#!/bin/bash

# Autor: GKW Agro Tech
# Titulares: 
# 	GKW Agro Tech
# 	MarcoA Instalacao de Sistemas de Aquecimento Ltda	
# Create Date: 11/11/2019
# Update Date: 19/11/2019
# Versao: 1.1
#
# Aplicacao responsavel por iniciar o servico de rede
# Definindo um IP e MASK especifico

sudo ifconfig wlan0 up 10.0.1.1 netmask 255.255.255.0
sudo hostapd /etc/hostapd/hostapd.conf
sudo service isc-dhcp-server restart
sudo service hostapd start
