from http import HTTPStatus


def test_create_pagamentos(client):
    response_pedido = client.post(
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

    assert response_pedido.status_code == HTTPStatus.CREATED

    pedido = response_pedido.json()

    response = client.post(
        '/pagamentos/',
        json={
            'pedido_id': pedido['pedido_id'],
            'status': 'Pago',
            'metodo': 'Cartão',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
