# Author: Junior Tada
from app.db import Base
from sqlalchemy import Integer, Column, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship


class Cliente(Base):
    __tablename__ = 'cliente'

    nome = Column(String)


class Produto(Base):
    __tablename__ = 'produto'

    nome = Column(String)
    preco = Column(DECIMAL(10,2))
    multiplo = Column(Integer)


class Item(Base):
    __tablename__ = 'item'

    # many-to-one produto-item
    produto_id = Column(Integer, ForeignKey('produto.id'))
    produto = relationship("Produto", backref="itens", lazy="joined")
    preco = Column(DECIMAL(10,2))
    total = Column(DECIMAL(10,2))
    quantidade = Column(Integer)
    # one-to-many pedido-item
    pedido_id = Column(Integer, ForeignKey('pedido.id'))
    rentabilidade = Column(String)


class Pedido(Base):
    __tablename__ = 'pedido'

    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    cliente = relationship("Cliente", backref="pedidos", lazy="joined")
    # many-to-one item-pedido
    itens = relationship("Item", backref="pedidos")