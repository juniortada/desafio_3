# Author: Junior Tada
from flask import Blueprint, request, render_template, jsonify
from app import log
from app.db import sessao


# Define o blueprint
pedidos = Blueprint('pedidos', __name__)
