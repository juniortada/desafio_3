# Author: Junior Tada
import unittest
import json
from app import app


class ProdutossTest(unittest.TestCase):
    """ Classe de teste do json que carrega produtos. """

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
        response = self.app.get('/financeiro/_produtos/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        produtos = {'produtos': [{'id': '1', 'multiplo': None, 'nome': 'Millenium Falcon', 'preco': '550000.00'}, {'id': '2', 'multiplo': 2, 'nome': 'X-Wing', 'preco': '60000.00'}, {'id': '3', 'multiplo': None, 'nome': 'Super Star Destroyer', 'preco': '4570000.00'}, {'id': '4', 'multiplo': 2, 'nome': 'TIE Fighter', 'preco': '75000.00'}, {'id': '5', 'multiplo': 5, 'nome': 'Lightsaber', 'preco': '6000.00'}, {'id': '6', 'multiplo': None, 'nome': 'DLT-19 Heavy Blaster Rifle', 'preco': '5800.00'}, {'id': '7', 'multiplo': 10, 'nome': 'DL-44 Heavy Blaster Pistol', 'preco': '1500.00'}, {'id': '8', 'multiplo': None, 'nome': 'Millenium Falcon', 'preco': '550000.00'}, {'id': '9', 'multiplo': 2, 'nome': 'X-Wing', 'preco': '60000.00'}, {'id': '10', 'multiplo': None, 'nome': 'Super Star Destroyer', 'preco': '4570000.00'}, {'id': '11', 'multiplo': 2, 'nome': 'TIE Fighter', 'preco': '75000.00'}, {'id': '12', 'multiplo': 5, 'nome': 'Lightsaber', 'preco': '6000.00'}, {'id': '13', 'multiplo': None, 'nome': 'DLT-19 Heavy Blaster Rifle', 'preco': '5800.00'}, {'id': '14', 'multiplo': 10, 'nome': 'DL-44 Heavy Blaster Pistol', 'preco': '1500.00'}]}
        dados = json.loads(response.data.decode('utf-8'))
        self.assertEqual(dados, produtos)