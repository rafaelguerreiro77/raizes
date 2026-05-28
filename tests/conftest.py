import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from raizes.app import app
from raizes.database import get_session
from raizes.models import Produto, Usuario, table_registry
from raizes.security import get_senha_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def usuario(session):
    senha = '12345678'
    usuario = Usuario(
        nome='Rafael',
        email='teste@raizes.com',
        endereco='teste',
        senha=get_senha_hash('12345678'),
        perfil='teste',
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    usuario.reseta_senha = senha

    return usuario


@pytest.fixture
def produto(session):
    produto = Produto(
        nome='Lanche',
        descricao='Pão Hamburguer, Carne, Queijo e alface',
        preco_unitario=10.05,
    )
    session.add(produto)
    session.commit()
    session.refresh(produto)
    return produto


@pytest.fixture
def token(client, usuario):
    response = client.post(
        '/auth/token/',
        data={'username': usuario.email, 'password': usuario.reseta_senha},
    )
    return response.json()['access_token']
