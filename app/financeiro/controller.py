# Author: Junior Tada
from flask import Blueprint, request, render_template, jsonify, flash, url_for, redirect, flash
from app.db import sessao, Dao
from app.financeiro.model import Cliente, Produto, Pedido, Item
from app import log
import json
from decimal import Decimal


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
    try:
        with sessao() as session:
            pedidos = Dao(session).todos(Pedido)
            return render_template('financeiro/pedido.html', pedidos=pedidos)
    except Exception as e:
        msg = 'Erro ao exibir pedidos!'
        log.exception(msg + str(e))
        flash(msg, 'alert-danger')
        return render_template('index.html')


@financeiro.route('/pedido/novo', methods=['GET', 'POST'])
def pedido_novo():
    try:
        if request.method == 'POST':
            pedido = Pedido()
            with sessao() as session:
                dao = Dao(session)
                if _salvar(pedido, dao):
                    flash('Pedido Salvo com Sucesso!', 'alert-success')
                    return redirect(url_for('financeiro.pedido'))
        return render_template('financeiro/pedido_novo.html')
    except Exception as e:
        msg = 'Erro ao salvar pedido!'
        log.exception(msg + str(e))
        flash(msg, 'alert-danger')
        return render_template('index.html')


@financeiro.route('/pedido/editar/<int:id>', methods=['GET', 'POST'])
def pedido_editar(id):
    try:
        with sessao() as session:
            dao = Dao(session)
            pedido = dao.buscarID(Pedido, int(id))
            if pedido:
                if request.method == 'POST':
                    if _salvar(pedido, dao):
                        flash('Pedido Alterado com Sucesso!', 'alert-success')
                        return redirect(url_for('financeiro.pedido'))
                itens = [{
                        'produto_id': str(item.produto_id), 'nome': item.produto.nome,
                        'quantidade': str(item.quantidade), 'preco': str(item.preco), 'total': str(item.total),
                        'rentabilidade': item.rentabilidade
                        } for item in pedido.itens] 
                dictPedido = {
                    'cliente': str(pedido.cliente_id),
                    'itens': itens
                }
                pedidoJson = json.dumps(dictPedido)
                return render_template('financeiro/pedido_novo.html', pedidoJson=pedidoJson)           
    except Exception as e:
        msg = 'Erro ao editar pedido!'
        log.exception(msg + str(e))
        flash(msg, 'alert-danger')
        return render_template('index.html')


def _salvar(pedido, dao):
    form = json.loads(request.form['pedidoJson'])
    print(form)
    if form:
        # cliente
        if form['cliente']:
            cliente = dao.buscarID(Cliente, int(form['cliente']))
            if cliente:
                pedido.cliente = cliente
        # limpa itens caso exista
        if pedido.itens:
            for i in pedido.itens:
                if i:
                    dao.excluir(i)
            pedido.itens.clear()
        # itens
        if form['itens']:
            for i in form['itens']:
                item = form['itens'][i]
                novo_item = Item()
                novo_item.produto_id = item['produto_id']
                novo_item.preco = Decimal(str(item['preco']))
                novo_item.total = Decimal(str(item['total']))
                novo_item.quantidade = int(item['quantidade'])
                novo_item.rentabilidade = item['rentabilidade']
                pedido.itens.append(novo_item)
        # salva no banco
        dao.salvar(pedido)
        return True