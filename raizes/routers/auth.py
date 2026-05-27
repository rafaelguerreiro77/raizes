from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from raizes.database import get_session
from raizes.models import Usuario
from raizes.schema import Token
from raizes.security import create_acesso_token, verifica_senha

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token/', response_model=Token)
def login_acesso_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    usuario = session.scalar(
        select(Usuario).where(Usuario.email == form_data.username)
    )

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='E-mail ou senha incorreto',
        )
    if not verifica_senha(form_data.password, usuario.senha):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Senha incorreta'
        )

    acesso_token = create_acesso_token(data={'sub': usuario.email})
    return {'acesso_token': acesso_token, 'tipo_token': 'bearer'}
