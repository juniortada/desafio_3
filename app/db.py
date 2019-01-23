# Author: Junior Tada
from sqlalchemy import create_engine, Integer, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from app import app, log
from contextlib import contextmanager

# Banco de dados
def conecta():
    """
    Método que conecta no banco de dados e cria engine.
    """
    global _engine
    _engine = create_engine(app.config['DB_URI'], echo=False)


@as_declarative()
class Base(object):
    """ 
    Classe Pai dos Objetos Model.
    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)


@contextmanager
def sessao():
    """ 
    Método para criar um escopo de transação. 
    :return:
    """
    session = sessionmaker(bind=_engine)()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        log.exception('Erro ao abrir sessão! ' + str(e))
        raise e
    finally:
        session.close()


class Dao(object):
    """
    Data Access Object. Classe Pai para acesso aos dados.
    :param session: Sessão para realizar uma transação no DB.
    """

    def __init__(self, session):
        self.session = session

    @staticmethod
    def criar_tabelas():
        """ 
        Método que cria todas as tabelas no DB.
        :return:
        """
        Base.metadata.create_all(_engine)
        
    def salvar(self, obj):
        """ 
        Método que salva objetos no DB. 
        :param obj: Objeto a ser salvo no DB.
        :return:
        """
        try:
            self.session.add(obj)
        except Exception as e:
            self._erro('Erro ao Salvar!', e)

    def alterar(self, obj, filtro):
        """ 
        Método para alterar objetos no DB. 
        :param obj: Objeto a ser alterado no DB.
        :param filtro: Filtro para pesquisar objeto a ser alterado. Ex: id=123
        :return:
        """
        try:
            self.session.query(obj.__class__).filter_by(**filtro).update(obj.__dict__)
        except Exception as e:
            self._erro('Erro ao Alterar!', e)

    def excluir(self, obj):
        """ 
        Método para excluir objetos no DB. 
        :param obj: Objeto a ser excluido no DB.
        :return:
        """
        try:
            self.session.delete(obj)
        except Exception as e:
            self._erro('Erro ao Excluir!', e)

    def todos(self, classe):
        """ 
        Método para buscar todos os objetos no DB.
        :param classe: Classe do objeto procurado. 
        :return: Lista com objetos encontrados.
        """
        try:
            return self.session.query(classe).all()
        except Exception as e:
            self._erro('Erro ao Buscar!', e)

    def buscarID(self, classe, id):
        """ 
        Método que retorna um objeto pelo ID. 
        :param classe: Classe do objeto procurado.
        :param id: ID do objeto procurado.
        :return: Objeto encontrado.
        """
        try:
            return self.session.query(classe).filter_by(id=id).first()
        except Exception as e:
            self._erro('Erro ao Buscar por ID!', e)


    def buscarLike(self, classe, **kwargs):
        """
        Método que busca a partir do atributo parecido(like).
           Ex: buscarLike(Cliente, nome='Luke')
        :param classe: Classe do objeto procurado.
        return: Lista com objetos match
        """
        try:
            for i in kwargs.items():
                atributo = i
            palavras = atributo[1].split(' ')
            attr = getattr(classe, atributo[0])  # pega a coluna pelo nome
            pesquisa = [attr.ilike('%{}%'.format(p)) for p in palavras]
            
            return self.session.query(classe).filter(*pesquisa).all()
        except Exception as e:
            self._erro('Erro ao Buscar Like!', e)


    def _erro(self, msg, erro):
        """ 
        Método executado quando ocorre erro nas ações com DB. 
        :param msg: Mensagem de erro.
        :param erro: Exception que causou o erro.
        :return:
        """
        log.exception(msg + str(erro))
        flash(msg, 'alert-danger')