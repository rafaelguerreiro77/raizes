from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from raizes.database import get_session
from raizes.models import Usuario
from raizes.schema import Message, Usuariolista, UsuarioPublico, UsuarioSchema
from raizes.security import get_senha_hash, get_usuario_logado

router = APIRouter(prefix='/usuarios', tags=['usuarios'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=UsuarioPublico
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

    senha_hashed = get_senha_hash(usuario.senha)
    db_usuario = Usuario(
        **usuario.model_dump(exclude={'senha'}),
        senha=senha_hashed,
    )

    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)

    return db_usuario


@router.get('/', response_model=Usuariolista)
def get_usuarios(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
):
    usuarios = session.scalars(select(Usuario).offset(skip).limit(limit)).all()
    return {'usuarios': usuarios}


@router.put('/{usuario_id}', response_model=UsuarioPublico)
def put_usuario(
    usuario_id: int,
    usuario: UsuarioSchema,
    session: Session = Depends(get_session),
    usuario_logado: Usuario = Depends(get_usuario_logado),
):
    if usuario_logado.usuario_id != usuario_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Não tem permissão'
        )
    try:
        usuario_logado.nome = usuario.nome
        usuario_logado.email = usuario.email
        usuario_logado.endereco = usuario.endereco
        usuario_logado.perfil = usuario.perfil
        usuario_logado.senha = get_senha_hash(usuario.senha)
        session.commit()
        session.refresh(usuario_logado)
        return usuario_logado
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Nome de usuário já existe'
        )


@router.get('/busca', response_model=Usuariolista)
def pesquisar_usuario(
    termo: str = Query(..., description='Buscar por id, nome ou email'),
    session: Session = Depends(get_session),
):
    query = select(Usuario)

    if termo.isdigit():
        query = query.where(Usuario.usuario_id == int(termo))
    else:
        query = query.where(
            or_(
                Usuario.nome.ilike(f'%{termo}%'),
                Usuario.email.ilike(f'%{termo}%'),
            )
        )

    usuarios = session.scalars(query).all()
    if not usuarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    return {'usuarios': usuarios}


@router.delete('/{usuario_id}', response_model=Message)
def delete_usuario(
    usuario_id: int,
    session: Session = Depends(get_session),
    usuario_logado: Usuario = Depends(get_usuario_logado),
):
    if usuario_logado.usuario_id != usuario_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Não tem permissão'
        )
    session.delete(usuario_logado)
    session.commit()
    return {'message': 'Usuário excluído com sucesso'}
