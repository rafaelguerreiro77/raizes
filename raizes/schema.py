from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


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


class Usuariolista(BaseModel):
    usuarios: list[UsuarioPublico]


class Pedido(BaseModel):
    usuario_id: int
    unidade_id: int
    status: str
    canal_pedido: str
    valor_pedido: Decimal
    data_pedido: datetime


class PedidoPublico(BaseModel):
    id: int
    usuario_id: int
    unidade_id: int
    status: str
    canal_pedido: str
    valor_pedido: Decimal
    data_pedido: datetime


class PedidoDB(Pedido):
    id: int


class PedidoLista(BaseModel):
    pedidos: list[PedidoPublico]
