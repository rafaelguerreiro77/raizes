from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from raizes.database import get_session
from raizes.models import ItemPedido
from raizes.schema import ItemPedidoLista, ItemPedidoPublico, ItemPedidoSchema

router = APIRouter(
    prefix='/itens_pedido',
    tags=['itens_pedido'],
)


@router.post(
    '/',
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


@router.get('/', response_model=ItemPedidoLista)
def get_itens_pedido(session: Session = Depends(get_session)):
    itens = session.scalars(select(ItemPedido)).all()
    return {'itens': itens}
