import json
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
load_dotenv()
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}
def conectar_db():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None  

def inserir_nota(dado):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute("INSERT INTO notas (link_nota) VALUES (%s)", (dado,))
    conexao.close()

def listar_notas():
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM notas WHERE consultada = false")
            notas = cursor.fetchall()
    conexao.close()
    return notas

def buscar_empresa(cnpj):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM empresas WHERE cnpj = %s", (cnpj,))
            empresa = cursor.fetchone()
    conexao.close()
    return empresa

def cadastrar_empresa(nome, cnpj):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute("INSERT INTO empresas (cnpj, nome_empresa) VALUES (%s, %s)", (cnpj, nome))
    conexao.close()

def buscar_produto_dicionario(codigo_produto, id_empresa):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM dicionario_produtos WHERE id_externo = %s AND empresa = %s", (codigo_produto, id_empresa))  
            produto = cursor.fetchone()
    conexao.close()
    return produto

def inserir_produto_dicionario(codigo_produto, nome_produto, id_empresa):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute("INSERT INTO dicionario_produtos (id_externo, nome_externo, empresa) VALUES (%s, %s, %s)", (codigo_produto, nome_produto, id_empresa))
    conexao.close()

def inserir_conteudo_nota(nf_registro, empresa, produto, quantidade, valor_unitario, valor_total, data_registro, UN):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute("INSERT INTO conteudo_nota (nf_registro, empresa, produto, quantidade, valor_unitario, valor_total, data_registro, un) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (nf_registro, empresa, produto, quantidade, valor_unitario, valor_total, data_registro, UN))
    conexao.close()
    
def concluir_consulta_nota(id_nota):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute("UPDATE notas SET consultada = true WHERE id_nota = %s", (id_nota,))
    conexao.close()

def dicionario_sem_produto():
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM dicionario_produtos WHERE id_produto_interno IS NULL ORDER BY nome_externo")
            produtos = cursor.fetchall()
    conexao.close()
    return produtos

def lista_produtos():
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM produtos JOIN unidade_medida ON produtos.unidade_medida = unidade_medida.id_um ORDER BY nome")
            produtos = cursor.fetchall()
    conexao.close()
    return produtos

def inserir_produto(nome_produto, un, quantidade):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute("INSERT INTO produtos (nome, unidade_medida, quantidade) VALUES (%s, %s, %s) RETURNING id_interno", (nome_produto, un, quantidade))
            id_produto = cursor.fetchone()[0]
    conexao.close()
    return id_produto

def associar_produto_dicionario(id_produto, id_dicionario):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute("UPDATE dicionario_produtos SET id_produto_interno = %s WHERE id_dicionario = %s", (id_produto, id_dicionario))
    conexao.close()