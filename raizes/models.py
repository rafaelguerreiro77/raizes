from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Usuario:
    __tablename__ = 'usuarios'

    usuario_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)
    endereco: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    perfil: Mapped[str]


@table_registry.mapped_as_dataclass
class Pedido:
    __tablename__ = 'pedidos'
    pedido_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.usuario_id'))
    unidade_id: Mapped[int]
    status: Mapped[str]
    canal_pedido: Mapped[str]
    valor_pedido: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    data_pedido: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now()
    )


@table_registry.mapped_as_dataclass
class Produto:
    __tablename__ = 'produtos'
    produto_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)
    descricao: Mapped[str]
    preco_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2))


@table_registry.mapped_as_dataclass
class Pagamento:
    __tablename__ = 'pagamentos'
    pedido_id: Mapped[int] = mapped_column(
        ForeignKey('pedidos.pedido_id'), primary_key=True
    )
    status: Mapped[str]
    metodo: Mapped[str]
    data_pagamento: Mapped[datetime] = mapped_column(
        DateTime, init=False, server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class ItemPedido:
    __tablename__ = 'itens_pedido'
    pedido_id: Mapped[int] = mapped_column(
        ForeignKey('pedidos.pedido_id'), primary_key=True
    )
    produto_id: Mapped[int] = mapped_column(
        ForeignKey('produtos.produto_id'), primary_key=True
    )
    quantidade: Mapped[int]
    preco_unitario: Mapped[float]
