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

def inserir_nota_db(dado):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute("INSERT INTO notas (link_nota) VALUES (%s)", (dado,))
    conexao.close()

def listar_notas_db():
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

def buscar_empresa_db(cnpj):
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

def cadastrar_empresa_db(nome, cnpj):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute("INSERT INTO empresas (cnpj, nome_empresa) VALUES (%s, %s)", (cnpj, nome))
    conexao.close()

def buscar_produto_dicionario_db(codigo_produto, id_empresa):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM dicionario_produtos WHERE id_externo = %s AND id_empresa = %s", (codigo_produto, id_empresa))  
            produto = cursor.fetchone()
    conexao.close()
    return produto

def inserir_produto_dicionario_db(codigo_produto, nome_produto, id_empresa):
    conexao = conectar_db()
    if conexao == None:
        print('falha na conexao com banco')
        return
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute("INSERT INTO dicionario_produtos (id_externo, nome_externo, empresa) VALUES (%s, %s, %s)", (codigo_produto, nome_produto, id_empresa))
    conexao.close()