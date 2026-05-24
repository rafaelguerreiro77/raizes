from http import HTTPStatus

from fastapi.testclient import TestClient

from raizes.app import app
from raizes.schema import UsuarioPublico

client = TestClient(app)


def test_create_usuario(client):
    response = client.post(
        '/usuarios',
        json={
            'nome': 'Rafael',
            'endereco': 'Dois Córregos SP',
            'email': 'teste@raizes.com.br',
            'senha': '12345',
            'perfil': 'adm',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'nome': 'Rafael',
        'endereco': 'Dois Córregos SP',
        'email': 'teste@raizes.com.br',
        'perfil': 'adm',
        'usuario_id': 1,
    }


def test_get_usuarios(client):
    response = client.get('/usuarios')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'usuarios': []}


def test_get_usuarios_with_usuarios(client, usuario):
    user_schema = UsuarioPublico.model_validate(usuario).model_dump()
    response = client.get('/usuarios/')
    assert response.json() == {'usuarios': [user_schema]}


def test_put_usuario(client):
    client.post(
        '/usuarios',
        json={
            'nome': 'Rafael',
            'endereco': 'Dois Córregos SP',
            'email': 'teste@raizes.com.br',
            'senha': '12345',
            'perfil': 'adm',
        },
    )

    response = client.put(
        '/usuarios/1',
        json={
            'nome': 'Rafael',
            'endereco': 'Dois Córregos SP',
            'email': 'teste@raizes.com.br',
            'perfil': 'adm',
            'senha': '12345',
        },
    )
    assert response.status_code == HTTPStatus.OK


def test_delete_usuario(client, usuario):
    response = client.delete('/usuarios/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário excluído com sucesso'}


def test_create_pedido(client):
    response = client.post(
        '/pedidos/',
        json={
            'usuario_id': 1,
            'unidade_id': 1,
            'status': 'Aguardando pagamento',
            'canal_pedido': 'App',
            'valor_pedido': 10.05,
            'data_pedido': '2020-01-01T00:00:00',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'usuario_id': 1,
        'unidade_id': 1,
        'status': 'Aguardando pagamento',
        'canal_pedido': 'App',
        'valor_pedido': '10.05',
        'data_pedido': '2020-01-01T00:00:00',
        'pedido_id': 1,
    }


def test_get_pedido(client):
    response = client.get('/pedidos/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'pedidos': []}


def test_get_pedido_pedido_id(client):
    client.post(
        '/pedidos/',
        json={
            'usuario_id': 1,
            'unidade_id': 1,
            'status': 'Aguardando pagamento',
            'canal_pedido': 'App',
            'valor_pedido': 10.05,
            'data_pedido': '2020-01-01T00:00:00',
        },
    )

    response = client.get('/pedidos/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'pedido_id': 1,
        'usuario_id': 1,
        'unidade_id': 1,
        'status': 'Aguardando pagamento',
        'canal_pedido': 'App',
        'valor_pedido': '10.05',
        'data_pedido': '2020-01-01T00:00:00',
    }


def test_get_pedido_id_not_found(client):
    response = client.get('/pedidos/999999999')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_produto(client):
    response = client.post(
        '/produtos/',
        json={
            'nome': 'Lanche',
            'descricao': 'Pão Hamburguer, Carne, Queijo e alface',
            'preco_unitario': 10.05,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'nome': 'Lanche',
        'descricao': 'Pão Hamburguer, Carne, Queijo e alface',
        'preco_unitario': '10.05',
        'produto_id': 1,
    }


def test_get_produto(client):
    response = client.get('/produtos/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'produtos': []}


def test_get_produto_id(client):
    client.post(
        '/produtos/',
        json={
            'nome': 'Lanche',
            'descricao': 'Pão Hamburguer, Carne, Queijo e alface',
            'preco_unitario': 10.05,
        },
    )
    response = client.get('/produtos/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'produto_id': 1,
        'nome': 'Lanche',
        'descricao': 'Pão Hamburguer, Carne, Queijo e alface',
        'preco_unitario': '10.05',
    }


def test_get_produtos_id_not_found(client):
    client.post(
        '/produtos',
        json={
            'nome': 'Lanche',
            'descricao': 'Pão Hamburguer, Carne, Queijo e alface',
            'preco_unitario': 10.05,
        },
    )
    response = client.get('/produtos/99999999')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_put_produto(client):
    client.post(
        '/produtos/',
        json={
            'nome': 'Lanche',
            'descricao': 'Pão Hamburguer, Carne, Queijo e alface',
            'preco_unitario': 10.05,
        },
    )

    response = client.put(
        '/produtos/1',
        json={
            'nome': 'Lanche',
            'descricao': 'Pão Hamburguer, Carne, Queijo e tomate',
            'preco_unitario': 20.00,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'nome': 'Lanche',
        'descricao': 'Pão Hamburguer, Carne, Queijo e tomate',
        'preco_unitario': '20.00',
        'produto_id': 1,
    }


def test_delete_produto(client, produto):
    response = client.delete('/produtos/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Produto excluído com sucesso'}


def test_create_pagamento_mock(client):
    response = client.post(
        '/pagamentos/mock',
        json={
            'pedido_id': 1,
            'status': 'Pago',
            'metodo': 'Cartão',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['pedido_id'] == 1
    assert data['status'] == 'Pago'
    assert data['metodo'] == 'Cartão'
    assert 'data_pagamento' in data


def test_create_item_pedido(client):
    response = client.post(
        '/itens_pedido/',
        json={
            'pedido_id': 1,
            'produto_id': 1,
            'quantidade': 1,
            'preco_unitario': 10.55,
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['pedido_id'] == 1
    assert data['produto_id'] == 1
    assert data['quantidade'] == 1
    assert data['preco_unitario'] == '10.55'


def test_get_itens_pedido(client):
    client.post(
        '/itens_pedido/',
        json={
            'pedido_id': 1,
            'produto_id': 1,
            'quantidade': 1,
            'preco_unitario': 10.55,
        },
    )

    response = client.get('/itens_pedido/')

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert len(data['itens']) == 1
    assert data['itens'][0]['pedido_id'] == 1
