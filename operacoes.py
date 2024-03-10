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
    
    opcao = int(input('escolha uma nota: '))
    link_nota = notas[opcao]['link_nota']
    dados = requisicao(link_nota)
    print(json.dumps(dados, indent=2))

def requisicao(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }
    try:
        requisicao = requests.get(link, headers=headers)
        html_content = requisicao.text
        soup = BeautifulSoup(html_content, 'html.parser')
        tabble = soup.find_all('table', class_='table table-striped')[0]
        dados = []
        for linha in tabble.find_all('tr'):
            cells = linha.find_all('td')
            if len(cells) > 0:
                nome_codigo = cells[0].text.strip().split("\n")
                nome = nome_codigo[0].strip()
                codigo = nome_codigo[1].split(":")[1].strip()
                quantidade = cells[1].text.split(":")[1].strip()
                un = cells[2].text.split(":")[1].strip()
                valor_total = cells[3].text.split("$")[1].strip()

                dados.append({
                    'nome': nome,
                    'codigo': codigo,
                    'quantidade': quantidade,
                    'un': un,
                    'valor_total': valor_total
                })
        return dados

    except Exception as e:
        print(f'erro ao fazer requisição: {e}')