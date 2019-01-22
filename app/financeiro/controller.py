# Author: Junior Tada
from flask import Blueprint, request, render_template, jsonify
from app import log
from app.db import sessao


# Define o blueprint
financeiro = Blueprint('financeiro', __name__)


@financeiro.route('/cliente', methods=['GET'])
def cliente():
    return render_template('financeiro/cliente.html')


@financeiro.route('/produto', methods=['GET'])
def produto():
    return render_template('financeiro/produto.html')


@financeiro.route('/pedido', methods=['GET', 'POST'])
def pedido():
    return render_template('financeiro/pedido.html')