# Author: Junior Tada
import unittest
import json
from app import app


class ClientesTest(unittest.TestCase):
    """ Classe de teste do json que carrega clientes. """

    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    def tearDown(self):
        pass

    def test_clientes(self):
        response = self.app.get('/financeiro/_clientes/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        clientes = {'clientes': [{'id': '1', 'nome': 'Darth Vader'}, {'id': '2', 'nome': 'Obi-Wan Kenobi'}, {'id': '3', 'nome': 'Luke Skywalker'}, {'id': '4', 'nome': 'Imperador Palpatine'}, {'id': '5', 'nome': 'Han Solo'}, {'id': '6', 'nome': 'Darth Vader'}, {'id': '7', 'nome': 'Obi-Wan Kenobi'}, {'id': '8', 'nome': 'Luke Skywalker'}, {'id': '9', 'nome': 'Imperador Palpatine'}, {'id': '10', 'nome': 'Han Solo'}]}
        dados = json.loads(response.data.decode('utf-8'))
        self.assertEqual(dados, clientes)