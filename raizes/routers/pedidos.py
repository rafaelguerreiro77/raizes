from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from raizes.database import get_session
from raizes.models import Pedido
from raizes.schema import PedidoLista, PedidoPublico, PedidoSchema

router = APIRouter(
    prefix='/pedidos',
    tags=['pedidos'],
)


@router.post('/', status_code=HTTPStatus.CREATED, response_model=PedidoPublico)
def create_pedido(
    pedido: PedidoSchema,
    session: Session = Depends(get_session),
):

    db_pedido = Pedido(**pedido.model_dump())

    session.add(db_pedido)
    session.commit()
    session.refresh(db_pedido)

    return db_pedido


@router.get('/', response_model=PedidoLista)
def get_pedidos(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    pedidos = session.scalars(select(Pedido).offset(skip).limit(limit)).all()
    return {'pedidos': pedidos}


@router.get('/{pedido_id}', response_model=PedidoPublico)
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


@router.get('/busca', response_model=PedidoLista)
def pesquisar_pedidos(
    canal_pedido: str = Query(..., description='Buscar pedidos por canal'),
    session: Session = Depends(get_session),
):
    pedidos = session.scalars(
        select(Pedido).where(Pedido.canal_pedido.ilike(f'%{canal_pedido}%'))
    ).all()

    if not pedidos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Nenhum pedido encontrado'
        )

    return {'pedidos': pedidos}
