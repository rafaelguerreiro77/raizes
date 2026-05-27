from fastapi import FastAPI

from raizes.routers import (
    auth,
    itens_pedido,
    pagamentos,
    pedidos,
    produtos,
    usuarios,
)

app = FastAPI()

app.include_router(usuarios.router)
app.include_router(auth.router)
app.include_router(pedidos.router)
app.include_router(produtos.router)

app.include_router(pagamentos.router)
app.include_router(itens_pedido.router)
