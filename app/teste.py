from app import get_uri
from app.db import sessao, Dao
from app.pedidos.model import Cliente, Produto
from datetime import datetime
from decimal import Decimal
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json


def criar_db():
    """ 
    Cria o banco de dados caso ele não exista.
    O nome do banco será o definido no config DB_URI. 
    """
    dados = get_uri()
    con = psycopg2.connect("dbname='postgres' user='"+dados['user']+"' host='localhost' password='"+dados['password']+"'")
    cur = con.cursor()
    cur.execute("select datname from pg_catalog.pg_database where datname='"+dados['db']+"'")
    if not bool(cur.rowcount):
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur.execute('CREATE DATABASE ' + dados['db'])
    cur.close()
    con.close()


def alterar_config():
    "Muda config CRIAR_DB para False"
    filel = __file__.replace('teste.py','')+'config.json'
    cfg = None
    with open(filel, 'r') as arq:
        cfg = json.loads(arq.read())
    if cfg is not None:
        cfg['CRIAR_DB'] = False
        with open(filel, 'w') as arq:
            arq.write(json.dumps(cfg, indent=2))


def criar_exemplos():
    """
    Método que cria dados fictícios para exemplo do desafio.
    """
    try:
        with sessao() as session:
            # abre sessao
            dao = Dao(session)
            # clientes
            cli1 = Cliente()
            cli1.nome = 'Darth Vader'
            dao.salvar(cli1)

            cli2 = Cliente()
            cli2.nome = 'Obi-Wan Kenobi'
            dao.salvar(cli2)

            cli3 = Cliente()
            cli3.nome = 'Luke Skywalker'
            dao.salvar(cli3)

            cli4 = Cliente()
            cli4.nome = 'Imperador Palpatine'
            dao.salvar(cli4)

            cli5 = Cliente()
            cli5.nome = 'Han Solo'
            dao.salvar(cli5)

            # produtos
            prod1 = Produto()
            prod1.nome = 'Millenium Falcon'
            prod1.preco = Decimal('550000')
            # prod1.multiplo = 0
            dao.salvar(prod1)

            prod2 = Produto()
            prod2.nome = 'X-Wing'
            prod2.preco = Decimal('60000')
            prod2.multiplo = 2
            dao.salvar(prod2)

            prod3 = Produto()
            prod3.nome = 'Super Star Destroyer'
            prod3.preco = Decimal('4570000')
            # prod3.multiplo = 0
            dao.salvar(prod3)

            prod4 = Produto()
            prod4.nome = 'TIE Fighter'
            prod4.preco = Decimal('75000')
            prod4.multiplo = 2
            dao.salvar(prod4)

            prod5 = Produto()
            prod5.nome = 'Lightsaber'
            prod5.preco = Decimal('6000')
            prod5.multiplo = 5
            dao.salvar(prod5)

            prod6 = Produto()
            prod6.nome = 'DLT-19 Heavy Blaster Rifle'
            prod6.preco = Decimal('5800')
            # prod6.multiplo = 2
            dao.salvar(prod6)

            prod7 = Produto()
            prod7.nome = 'DL-44 Heavy Blaster Pistol'
            prod7.preco = Decimal('1500')
            prod7.multiplo = 10
            dao.salvar(prod7)

    except Exception as e:
        raise e