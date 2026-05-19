from pydantic import BaseModel, EmailStr


class Usuario(BaseModel):
    nome: str
    endereco: str
    email: EmailStr
    senha: str
    perfil: str


class UsuarioPublico(BaseModel):
    id: int
    nome: str
    endereco: str
    email: EmailStr
    perfil: str


class UsuarioDB(Usuario):
    id: int
