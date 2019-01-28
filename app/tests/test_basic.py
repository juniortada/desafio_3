# Author: Junior Tada
import unittest
from app import app


class BasicTest(unittest.TestCase):
    """
    Classe de teste de exibição das páginas. 
    Verifica se todas as páginas da aplicação estão sendo exibidas.
    """

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

    def test_index(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_produto(self):
        response = self.app.get('/financeiro/produto', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_cliente(self):
        response = self.app.get('/financeiro/cliente', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_pedido(self):
        response = self.app.get('/financeiro/pedido', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_pedido_novo(self):
        response = self.app.get('/financeiro/pedido/novo', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    if __name__ == "__main__":
        unittest.main()