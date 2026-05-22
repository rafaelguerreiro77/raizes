from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from raizes.schema import (
    Message,
    Pedido,
    PedidoDB,
    PedidoLista,
    PedidoPublico,
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
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    user_with_id = UsuarioDB(**usuario.model_dump(), id=usuario_id)
    database[usuario_id - 1] = user_with_id
    return user_with_id


@app.delete('/usuarios/{usuario_id}', response_model=Message)
def delete_usuario(usuario_id: int):
    if usuario_id > len(database) or usuario_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    del database[usuario_id - 1]
    return {'message': 'Usuário excluido com sucesso'}


@app.post(
    '/pedidos/', status_code=HTTPStatus.CREATED, response_model=PedidoPublico
)
def create_pedido(pedido: Pedido):
    pedido_with_id = PedidoDB(**pedido.model_dump(), id=len(database) + 1)

    database.append(pedido_with_id)

    return pedido_with_id


@app.get('/pedidos/', response_model=PedidoLista)
def get_pedidos():
    return {'pedidos': database}


@app.get('/pedidos/{pedido_id}', response_model=PedidoPublico)
def get_pedido(pedido_id: int):
    if pedido_id > len(database) or pedido_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Pedido não encontrado'
        )

    return database[pedido_id - 1]
