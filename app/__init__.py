# Author: Junior Tada
from flask import Flask, render_template
import logging
from logging.handlers import RotatingFileHandler
import locale
import re

# Define app Flask
app = Flask(__name__)
__version__ = '0.1'
__author__ = 'Junior Tada'

# Configurações
app.config.from_json("config.json")

# Log Erro
formatter = logging.Formatter('%(levelname)s: %(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=1)
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
log = app.logger

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# HTTP error handling
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Principal
from app.controller import main

# Blueprints
from app.financeiro.controller import financeiro

# Registra blueprints
app.register_blueprint(financeiro, url_prefix='/financeiro')

# Define o locale BR
def setlocale():
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')
    except:
        locale.setlocale(locale.LC_ALL, 'portuguese_brazil')

def get_uri():
    """
    Método que retorna um dicionario com os dados da URI de conexão com o banco de dados.
    :return: dict com informações user, password, host e db_name
    """
    uri = app.config['DB_URI']
    user, password = re.search('//(.*)@', uri).group(1).split(':')
    host, db = re.search('@(.*)', uri).group(1).split('/')
    return {'user': user, 'password': password, 'host': host, 'db': db}

def _conecta():
    from app.db import conecta
    conecta()

# Cria o banco de dados e gera dados fictícios para exemplo do desafio.
if app.config['CRIAR_DB']:
    from app.db import Dao
    from app.teste import criar_exemplos, criar_db, alterar_config
    criar_db()
    _conecta()
    Dao.criar_tabelas()
    criar_exemplos()
    alterar_config()
else:
    _conecta()