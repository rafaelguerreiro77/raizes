from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from raizes.schema import (
    Message,
    Usuario,
    UsuarioDB,
    Usuariolista,
    UsuarioPublico,
)

app = FastAPI()

database = []


@app.post(
    '/usuarios/', status_code=HTTPStatus.CREATED, response_model=UsuarioPublico
)
def create_usuario(usuario: Usuario):
    user_with_id = UsuarioDB(**usuario.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get('/usuarios/', response_model=Usuariolista)
def get_usuarios():
    return {'usuarios': database}


@app.put('/usuarios/{usuario_id}', response_model=UsuarioPublico)
def put_usuario(usuario_id: int, usuario: Usuario):
    if usuario_id > len(database) or usuario_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuario não encontrado'
        )
    user_with_id = UsuarioDB(**usuario.model_dump(), id=usuario_id)
    database[usuario_id - 1] = user_with_id
    return user_with_id


@app.delete('/usuarios/{usuario_id}', response_model=Message)
def delete_usuario(usuario_id: int):
    if usuario_id > len(database) or usuario_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuario não encontrado'
        )
    del database[usuario_id - 1]
    return {'message': 'Usuario excluido com sucesso'}
