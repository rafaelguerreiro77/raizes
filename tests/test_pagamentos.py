from http import HTTPStatus


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
