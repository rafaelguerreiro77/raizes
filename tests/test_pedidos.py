from http import HTTPStatus


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


def test_delete_pedido(client):
    response_create = client.post(
        '/pedidos/',
        json={
            'usuario_id': 1,
            'unidade_id': 1,
            'status': 'pendente',
            'canal_pedido': 'app',
            'valor_pedido': 10,
            'data_pedido': '2026-01-01T00:00:00',
        },
    )

    assert response_create.status_code == HTTPStatus.CREATED

    pedido = response_create.json()

    response = client.delete(f'/pedidos/{pedido["pedido_id"]}')

    assert response.status_code == HTTPStatus.OK
