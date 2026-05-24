from datetime import datetime
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from raizes.database import get_session
from raizes.models import ItemPedido, Pagamento, Pedido, Produto, Usuario
from raizes.schema import (
    ItemPedidoLista,
    ItemPedidoPublico,
    ItemPedidoSchema,
    Message,
    PagamentoPublico,
    PagamentoSchema,
    PedidoLista,
    PedidoPublico,
    PedidoSchema,
    ProdutoLista,
    ProdutoPublico,
    ProdutoSchema,
    Usuariolista,
    UsuarioPublico,
    UsuarioSchema,
)

app = FastAPI()

database = []


@app.post(
    '/usuarios/', status_code=HTTPStatus.CREATED, response_model=UsuarioPublico
)
def create_usuario(
    usuario: UsuarioSchema, session: Session = Depends(get_session)
):
    db_usuario = session.scalar(
        select(Usuario).where(
            (Usuario.nome == usuario.nome) | (Usuario.email == usuario.email)
        )
    )

    if db_usuario:
        if db_usuario.nome == usuario.nome:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Nome já existente',
            )
        elif db_usuario.email == usuario.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='E-mail já existe',
            )

    db_usuario = Usuario(**usuario.model_dump())

    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)

    return db_usuario


@app.get('/usuarios/', response_model=Usuariolista)
def get_usuarios(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    usuarios = session.scalars(select(Usuario).offset(skip).limit(limit)).all()
    return {'usuarios': usuarios}


@app.put('/usuarios/{usuario_id}', response_model=UsuarioPublico)
def put_usuario(
    usuario_id: int,
    usuario: UsuarioSchema,
    session: Session = Depends(get_session),
):
    db_usuario = session.scalar(
        select(Usuario).where(Usuario.usuario_id == usuario_id)
    )
    if not db_usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Ususário não encontrado'
        )
    try:
        db_usuario.nome = usuario.nome
        db_usuario.email = usuario.email
        db_usuario.endereco = usuario.endereco
        db_usuario.perfil = usuario.perfil
        db_usuario.senha = usuario.senha
        session.commit()
        session.refresh(db_usuario)
        return db_usuario
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Nome de usuário já existe'
        )


@app.delete('/usuarios/{usuario_id}', response_model=Message)
def delete_usuario(usuario_id: int, session: Session = Depends(get_session)):
    db_usuario = session.scalar(
        select(Usuario).where(Usuario.usuario_id == usuario_id)
    )
    if not db_usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    session.delete(db_usuario)
    session.commit()
    return {'message': 'Usuário excluído com sucesso'}


@app.post(
    '/pedidos/', status_code=HTTPStatus.CREATED, response_model=PedidoPublico
)
def create_pedido(
    pedido: PedidoSchema,
    session: Session = Depends(get_session),
):

    db_pedido = Pedido(**pedido.model_dump())

    session.add(db_pedido)
    session.commit()
    session.refresh(db_pedido)

    return db_pedido


@app.get('/pedidos/', response_model=PedidoLista)
def get_pedidos(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    pedidos = session.scalars(select(Pedido).offset(skip).limit(limit)).all()
    return {'pedidos': pedidos}


@app.get('/pedidos/{pedido_id}', response_model=PedidoPublico)
def get_pedido(
    pedido_id: int,
    session: Session = Depends(get_session),
):
    pedido = session.get(Pedido, pedido_id)

    if not pedido:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Pedido não encontrado'
        )

    return pedido


@app.post(
    '/produtos/', status_code=HTTPStatus.CREATED, response_model=ProdutoPublico
)
def create_produto(
    produto: ProdutoSchema, session: Session = Depends(get_session)
):
    db_produto = session.scalar(
        select(Produto).where(Produto.nome == produto.nome)
    )
    if db_produto:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Nome de produto ja existe',
        )
    db_produto = Produto(**produto.model_dump())
    session.add(db_produto)
    session.commit()
    session.refresh(db_produto)
    return db_produto


@app.get('/produtos/', response_model=ProdutoLista)
def get_produto(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    produtos = session.scalars(select(Produto).offset(skip).limit(limit)).all()
    return {'produtos': produtos}


@app.get('/produtos/{produto_id}', response_model=ProdutoPublico)
def get_produtos(produto_id: int, session: Session = Depends(get_session)):
    produto = session.get(Produto, produto_id)

    if not produto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Produto não encontrado',
        )

    return produto


@app.put('/produtos/{produto_id}', response_model=ProdutoPublico)
def put_produto(
    produto_id: int,
    produto: ProdutoSchema,
    session: Session = Depends(get_session),
):
    db_produto = session.get(Produto, produto_id)
    if not db_produto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Produto não encontrado'
        )
    for key, value in produto.model_dump().items():
        setattr(db_produto, key, value)
    session.commit()
    session.refresh(db_produto)
    return db_produto


@app.delete('/produtos/{produto_id}')
def delete_produto(
    produto_id: int,
    session: Session = Depends(get_session),
):
    db_produto = session.get(Produto, produto_id)
    if not db_produto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Produto não encontrado'
        )
    session.delete(db_produto)
    session.commit()
    return {'message': 'Produto excluído com sucesso'}


# Endpoint real do pagamento
@app.post(
    '/pagamentos/',
    status_code=HTTPStatus.CREATED,
    response_model=PagamentoPublico,
)
def create_pagamento(
    pagamento: PagamentoSchema, session: Session = Depends(get_session)
):
    pedido = session.get(Pedido, pagamento.pedido_id)
    if not pedido:
        raise HTTPException(404, 'Pedido não encontrado')
    db_pagamento = session.get(Pagamento, pagamento.pedido_id)
    if db_pagamento:
        raise HTTPException(409, 'Pagamento já existe para este pedido')
    db_pagamento = Pagamento(**pagamento.model_dump())
    session.add(db_pagamento)
    session.commit()
    session.refresh(db_pagamento)
    return db_pagamento


# Endpoint mock para simulação de pagamento,
# sem banco de dados e validação externa
@app.post(
    '/pagamentos/mock',
    status_code=HTTPStatus.CREATED,
    response_model=PagamentoPublico,
)
def create_pagamento_mock(pagamento: PagamentoSchema):
    return {
        'pedido_id': pagamento.pedido_id,
        'status': 'Pago',
        'metodo': pagamento.metodo,
        'data_pagamento': datetime.now(),
    }


@app.post(
    '/itens_pedido/',
    status_code=HTTPStatus.CREATED,
    response_model=ItemPedidoPublico,
)
def create_item_pedido(
    item: ItemPedidoSchema,
    session: Session = Depends(get_session),
):
    db_item = session.get(ItemPedido, (item.pedido_id, item.produto_id))

    if db_item:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Item já existe no pedido'
        )

    db_item = ItemPedido(**item.model_dump())

    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


@app.get('/itens_pedido/', response_model=ItemPedidoLista)
def get_itens_pedido(session: Session = Depends(get_session)):
    itens = session.scalars(select(ItemPedido)).all()
    return {'itens': itens}
