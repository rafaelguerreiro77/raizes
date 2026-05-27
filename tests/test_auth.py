from http import HTTPStatus


def test_post_token(client, usuario):
    response = client.post(
        '/auth/token/',
        data={'username': usuario.email, 'password': usuario.reseta_senha},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'acesso_token' in token
    assert 'tipo_token' in token
