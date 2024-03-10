from db import inserir_nota_db, listar_notas_db
import requests
from bs4 import BeautifulSoup
import json

def inserir_nota():
    link_nota = input('link da nota: ')
    inserir_nota_db(link_nota)
    print('nota inserida com sucesso')

def consulta_nota():
    notas = listar_notas_db()
    cont = 0
    for nota in notas:
        print(cont)
        print(nota['link_nota'])
        cont += 1
    

