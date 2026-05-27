from http import HTTPStatus

from jwt import decode

from raizes.security import create_acesso_token, settings


def test_jwt():
    data = {'test': 'test'}
    token = create_acesso_token(data)

    decoded = decode(token, settings.CHAVE, algorithms=[settings.ALGORITMO])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/usuarios/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'não foi possível validar as credenciais'
    }
