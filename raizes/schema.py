from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UsuarioSchema(BaseModel):
    nome: str
    endereco: str
    email: EmailStr
    senha: str
    perfil: str


class UsuarioPublico(BaseModel):
    usuario_id: int
    nome: str
    endereco: str
    email: EmailStr
    perfil: str
    model_config = ConfigDict(from_attributes=True)


class Usuariolista(BaseModel):
    usuarios: list[UsuarioPublico]


class PedidoSchema(BaseModel):
    usuario_id: int
    unidade_id: int
    status: str
    canal_pedido: str
    valor_pedido: Decimal
    data_pedido: datetime


class PedidoPublico(BaseModel):
    pedido_id: int
    usuario_id: int
    unidade_id: int
    status: str
    canal_pedido: str
    valor_pedido: Decimal
    data_pedido: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class PedidoLista(BaseModel):
    pedidos: list[PedidoPublico]


class ProdutoSchema(BaseModel):
    nome: str
    descricao: str
    preco_unitario: Decimal


class ProdutoPublico(BaseModel):
    produto_id: int
    nome: str
    descricao: str
    preco_unitario: Decimal


class ProdutoDB(ProdutoSchema):
    produto_id: int


class ProdutoLista(BaseModel):
    produtos: list[ProdutoPublico]


class ItemPedidoSchema(BaseModel):
    pedido_id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal


class ItemPedidoPublico(BaseModel):
    pedido_id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal


class ItemPedidoLista(BaseModel):
    itens: list[ItemPedidoPublico]


class PagamentoSchema(BaseModel):
    pedido_id: int
    status: str
    metodo: str


class PagamentoPublico(BaseModel):
    pedido_id: int
    status: str
    metodo: str
    data_pagamento: datetime


class PagamentoLista(BaseModel):
    pagamentos: list[PagamentoPublico]


class Token(BaseModel):
    access_token: str
    token_type: str
