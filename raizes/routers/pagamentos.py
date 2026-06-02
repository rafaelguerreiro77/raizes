from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from raizes.database import get_session
from raizes.models import Pagamento, Pedido
from raizes.schema import PagamentoPublico, PagamentoSchema

router = APIRouter(
    prefix='/pagamentos',
    tags=['pagamentos'],
)


@router.post(
    '/',
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

    status = pagamento.status.lower()

    if status in {'pago', 'aprovado'}:
        pedido.status = 'pago'
    elif status in {'recusado', 'negado'}:
        pedido.status = 'cancelado'

    session.add(db_pagamento)
    session.commit()
    session.refresh(db_pagamento)

    return db_pagamento
