"""
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 19/11/2019

Funcao que tem por realizar a conexao com o banco de dados do sistema
"""

import psycopg2 as pdb


# SET UP THE CONNECTION
try:
    connection = pdb.connect(database="marcoa", user="postgres", password="marcoA345", host="127.0.0.1", port="5432")
    #connection = pdb.connect(database="marcoa", user="postgres", password="12345", host="127.0.0.1", port="5432")

except (Exception, pdb.Error) as error:
        print("Error connect database", error)
        sys.exit(1)
