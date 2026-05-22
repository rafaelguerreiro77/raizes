from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, func
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
    usuario_id: Mapped[int]
    unidade_id: Mapped[int]
    status: Mapped[str]
    canal_pedido: Mapped[str]
    valor_pedido: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    data_pedido: Mapped[datetime] = mapped_column(
        DateTime, init=False, server_default=func.now()
    )
