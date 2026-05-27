from http import HTTPStatus


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
