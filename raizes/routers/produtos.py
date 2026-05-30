from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from raizes.database import get_session
from raizes.models import Produto
from raizes.schema import ProdutoLista, ProdutoPublico, ProdutoSchema

router = APIRouter(
    prefix='/produtos',
    tags=['produtos'],
)


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=ProdutoPublico
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


@router.get('/', response_model=ProdutoLista)
def get_produto(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    produtos = session.scalars(select(Produto).offset(skip).limit(limit)).all()
    return {'produtos': produtos}


@router.get('/busca', response_model=ProdutoLista)
def pesquisar_produtos(
    session: Session = Depends(get_session),
    termo: str = Query(..., description='Buscar por id ou nome'),
):
    query = select(Produto)
    if termo.isdigit():
        query = query.where(Produto.produto_id == int(termo))
    else:
        query = query.where(Produto.nome.ilike(f'%{termo}%'))
    produtos = session.scalars(query).all()
    if not produtos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Produto não encontrado'
        )
    return {'produtos': produtos}


@router.put('/{produto_id}', response_model=ProdutoPublico)
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


@router.delete('/{produto_id}')
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
