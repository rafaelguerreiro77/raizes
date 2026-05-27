from datetime import datetime
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


# Endpoint real do pagamento
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
    session.add(db_pagamento)
    session.commit()
    session.refresh(db_pagamento)
    return db_pagamento


# Endpoint mock para simulação de pagamento,
# sem banco de dados e validação externa
@router.post(
    '/mock',
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
