import db as database
import requests
from bs4 import BeautifulSoup
import json
import time
import random

def inserir_nota():
    link_nota = input('link da nota: ')
    database.inserir_nota(link_nota)
    print('nota inserida com sucesso')

def consulta_nota():
    notas = database.listar_notas()
    cont = 0
    for nota in notas:
        dados = requisicao(nota['link_nota'])
        data = ((dados[0]['data_emissao']).split(' '))[0]

        try:
            id_empresa = database.buscar_empresa(dados[0]['cnpj'])['id_empresa']
        except:
            database.cadastrar_empresa(dados[0]['nome'], dados[0]['cnpj'])
            id_empresa = database.buscar_empresa(dados[0]['cnpj'])['id_empresa']

        for produto in dados[0]['tabela']:
            try:
                id_produto = database.buscar_produto_dicionario(produto['codigo'],id_empresa)['id_dicionario']
            except:
                database.inserir_produto_dicionario(produto['codigo'], produto['nome'], id_empresa)
                id_produto = database.buscar_produto_dicionario(produto['codigo'],id_empresa)['id_dicionario']
            if produto['quantidade'] != 1:
                valor_unitario = round((produto['valor_total'] / produto['quantidade']), 2)
                database.inserir_conteudo_nota(nota['id_nota'], id_empresa, id_produto, produto['quantidade'], valor_unitario, produto['valor_total'], data, produto['un'])
            else:
                database.inserir_conteudo_nota(nota['id_nota'], id_empresa, id_produto, produto['quantidade'], produto['valor_total'], produto['valor_total'], data, produto['un'])
        database.concluir_consulta_nota(nota['id_nota'])
        espera = round(random.uniform(5, 9), 2)
        print(f'Aguardando {espera} segundos...')
        time.sleep(espera)        


def requisicao(link):
    # cabecario para simular um navegador pois alguns sites bloqueiam requisições de bots
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }
    try:
        requisicao = requests.get(link, headers=headers)
        html_content = requisicao.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # tratamento dos dados pensando na fazenda.mg

        tabble = soup.find_all('table', class_='table table-striped')[0]


        nome_empresa = soup.find('th', class_='text-center text-uppercase').text.strip()


        info_empresa = (
                soup.find(
                    'td', style=lambda value: value and 'border-top: 0px;' in value
                ).text.strip()
            ).split(', ')


        cnpj = info_empresa[0].replace('CNPJ: ', '').strip()


        dados = []
        informacoes_gerais = soup.find_all('table', class_='table table-hover')[5]

        data_emissao = informacoes_gerais.find_all('tr')[1].find_all('td')[3].text.strip()

        tabela = []
        for linha in tabble.find_all('tr'):
            cells = linha.find_all('td')
            if len(cells) > 0:
                # quebrando os dados
                nome_codigo = cells[0].text.strip().split("\n")
                nome = nome_codigo[0].strip()
                codigo = (nome_codigo[1].split(":")[1].strip()).replace(')', '')
                quantidade = cells[1].text.split(":")[1].strip()
                un = cells[2].text.split(":")[1].strip()
                valor_bruto = (cells[3].text.split("R$:")[1].strip()).replace('R$', '').strip()
                valor_total = float(valor_bruto.replace(',', '.'))

                tabela.append({
                    'nome': nome,
                    'codigo': int(codigo),
                    'quantidade': float(quantidade),
                    'un': un,
                    'valor_total': valor_total
                })
        dados.append({
            'tabela': tabela,
            'nome': nome_empresa,
            'cnpj': cnpj,
            'data_emissao': data_emissao
        })
        return dados

    except Exception as e:
        print(f'erro ao fazer requisição: {e}')

def unificar_produtos():
    dados = database.dicionario_sem_produto()
    produtos = database.lista_produtos()
    for dicionario in dados:
        
        print('produtos disponíveis:')
        for produto in produtos:
            print(produto['id_interno'])
            print(produto['nome'], produto['nome_um'], produto['quantidade'])
            print('-------------------')
        print(dicionario['nome_externo'])
        opcao = input('digite o id do produto que deseja associar ao dicionario ou 0 para criar um novo: ')
        if opcao == '':
            break
        if int(opcao) < 0:
            continue
        if int(opcao) == 0:
            nome = input('digite o nome do produto: ')
            un = input('digite a unidade de medida: ')
            quantidade = input('digite a quantidade: ')
            id_produto = database.inserir_produto(nome, un, quantidade)
            database.associar_produto_dicionario(id_produto, dicionario['id_dicionario'])
            produtos = database.lista_produtos()
        if int(opcao) > 0:
            database.associar_produto_dicionario(opcao, dicionario['id_dicionario'])

            

