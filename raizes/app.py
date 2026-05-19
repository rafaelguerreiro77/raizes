from http import HTTPStatus

from fastapi import FastAPI

from raizes.schema import Usuario, UsuarioDB, UsuarioPublico

app = FastAPI()

database = []


@app.post(
    '/usuarios/', status_code=HTTPStatus.CREATED, response_model=UsuarioPublico
)
def create_usuario(usuario: Usuario):
    user_with_id = UsuarioDB(**usuario.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id
