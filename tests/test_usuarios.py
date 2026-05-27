from http import HTTPStatus

from raizes.schema import UsuarioPublico


def test_create_usuario(client):
    response = client.post(
        '/usuarios',
        json={
            'nome': 'Rafael',
            'endereco': 'Dois Córregos SP',
            'email': 'teste@raizes.com.br',
            'perfil': 'adm',
            'senha': '12345',
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


def test_put_usuario(client, usuario, token):
    response = client.put(
        f'/usuarios/{usuario.usuario_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'nome': 'Rafael',
            'endereco': 'Dois Córregos SP',
            'email': 'teste@raizes.com.br',
            'perfil': 'adm',
            'senha': '12345',
        },
    )
    assert response.status_code == HTTPStatus.OK


def test_delete_usuario(client, usuario, token):
    response = client.delete(
        f'/usuarios/{usuario.usuario_id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário excluído com sucesso'}
