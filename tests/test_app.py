from http import HTTPStatus

from fastapi.testclient import TestClient

from raizes.app import app

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
        'id': 1,
    }


def test_get_usuarios(client):
    response = client.get('/usuarios')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'usuarios': [
            {
                'nome': 'Rafael',
                'endereco': 'Dois Córregos SP',
                'email': 'teste@raizes.com.br',
                'perfil': 'adm',
                'id': 1,
            }
        ]
    }


def test_put_usuario(client):
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
    assert response.json() == {
        'nome': 'Rafael',
        'endereco': 'Dois Córregos SP',
        'email': 'teste@raizes.com.br',
        'perfil': 'adm',
        'id': 1,
    }


def test_delete_usuario(client):
    response = client.delete('/usuarios/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuario excluido com sucesso'}
