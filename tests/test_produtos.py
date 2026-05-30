from http import HTTPStatus


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


def test_get_produto_busca(client):
    client.post(
        '/produtos/',
        json={
            'nome': 'Lanche',
            'descricao': 'Pão Hamburguer, Carne, Queijo e alface',
            'preco_unitario': 10.05,
        },
    )

    response = client.get('/produtos/busca?termo=1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'produtos': [
            {
                'produto_id': 1,
                'nome': 'Lanche',
                'descricao': 'Pão Hamburguer, Carne, Queijo e alface',
                'preco_unitario': '10.05',
            }
        ]
    }


def test_get_produtos_busca_not_found(client):
    response = client.get('/produtos/busca?termo=naoexiste')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Produto não encontrado'}


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
