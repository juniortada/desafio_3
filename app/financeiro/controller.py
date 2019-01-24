# Author: Junior Tada
from flask import Blueprint, request, render_template, jsonify, flash
from app.db import sessao, Dao
from app.financeiro.model import Cliente, Produto
from app import log


# Define o blueprint
financeiro = Blueprint('financeiro', __name__)


@financeiro.route('/cliente', methods=['GET'])
def cliente():
    try:
        with sessao() as session:
            clientes = Dao(session).todos(Cliente)
            return render_template('financeiro/cliente.html', clientes=clientes)
    except Exception as e:
        msg = 'Erro ao exibir clientes!'
        log.exception(msg + str(e))
        flash(msg, 'alert-danger')
        return render_template('index.html')


@financeiro.route('/_clientes/', methods=['GET', 'POST'])
def _clientes():
    try:
        with sessao() as session:
            clientes = Dao(session).todos(Cliente)
            clientes = [{"id":str(i.id),"nome":i.nome} for i in clientes]
            return jsonify(clientes=clientes)
    except Exception as e:
        log.exception('Erro ajax clientes!' + str(e))


@financeiro.route('/produto', methods=['GET'])
def produto():
    try:
        with sessao() as session:
            produtos = Dao(session).todos(Produto)
            return render_template('financeiro/produto.html', produtos=produtos)
    except Exception as e:
        msg = 'Erro ao exibir produtos!'
        log.exception(msg + str(e))
        flash(msg, 'alert-danger')
        return render_template('index.html')


@financeiro.route('/_produtos/', methods=['GET', 'POST'])
def _produtos():
    try:
        with sessao() as session:
            produtos = Dao(session).todos(Produto)
            produtos = [{"id":str(i.id),"nome":i.nome, "preco":i.preco, "multiplo":i.multiplo} for i in produtos]
            return jsonify(produtos=produtos)
    except Exception as e:
        log.exception('Erro ajax produtos!' + str(e))


@financeiro.route('/pedido', methods=['GET'])
def pedido():
    return render_template('financeiro/pedido.html')


@financeiro.route('/pedido/novo', methods=['GET', 'POST'])
def pedido_novo():
    return render_template('financeiro/pedido_novo.html')


@financeiro.route('/pedido/editar/<int:id>', methods=['GET', 'POST'])
def pedido_editar(id):
    return render_template('financeiro/pedido_novo.html')