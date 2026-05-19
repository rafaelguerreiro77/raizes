from http import HTTPStatus

from fastapi.testclient import TestClient

from raizes.app import app

client = TestClient(app)


def test_create_usuario():
    client = TestClient(app)
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
        'id': 1,
    }
