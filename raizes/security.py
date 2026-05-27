from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from raizes.database import get_session
from raizes.models import Usuario
from raizes.settings import Settings

settings = Settings()

pwd_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def create_acesso_token(data: dict):
    codificar = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.TOKEN_EXPIRA
    )
    codificar.update({'exp': expire})
    codificar_jwt = encode(
        codificar, settings.CHAVE, algorithm=settings.ALGORITMO
    )
    return codificar_jwt


def get_senha_hash(senha: str):
    return pwd_hash.hash(senha)


def verifica_senha(senha_original: str, senha_hashed: str):
    return pwd_hash.verify(senha_original, senha_hashed)


def get_usuario_logado(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='não foi possível validar as credenciais',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(
            token, settings.CHAVE, algorithms=[settings.ALGORITMO]
        )
        subject_email = payload.get('sub')

        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    user = session.scalar(
        select(Usuario).where(Usuario.email == subject_email)
    )

    if not user:
        raise credentials_exception

    return user
