# Author: Junior Tada
from flask import Blueprint, request, render_template, jsonify, flash
from app.db import sessao, Dao
from app.financeiro.model import Cliente
from app import log


# Define o blueprint
financeiro = Blueprint('financeiro', __name__)


@financeiro.route('/cliente', methods=['GET'])
def cliente():
    try:
        with sessao() as session:
            dao = Dao(session)
            # import pdb
            # pdb.set_trace()
            clientes = dao.todos(Cliente)
            return render_template('financeiro/cliente.html', clientes=clientes)
    except Exception as e:
        msg = 'Erro ao exibir clientes!'
        log.exception(msg + str(e))
        flash(msg, 'alert-danger')
        return render_template('index.html')


@financeiro.route('/produto', methods=['GET'])
def produto():
    return render_template('financeiro/produto.html')


@financeiro.route('/pedido', methods=['GET', 'POST'])
def pedido():
    return render_template('financeiro/pedido.html')