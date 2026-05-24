from sqlalchemy import select

from raizes.models import ItemPedido, Pagamento, Pedido, Usuario


def test_create_usuario(session):
    new_usuario = Usuario(
        nome='Rafael',
        endereco='Dois Córregos SP',
        email='teste@raizes.com.br',
        senha='12345',
        perfil='adm',
    )
    session.add(new_usuario)
    session.commit()

    usuario = session.scalar(select(Usuario).where(Usuario.nome == 'Rafael'))
    assert usuario.nome == 'Rafael'


def test_create_pedido(session):
    new_pedido = Pedido(
        usuario_id=1,
        unidade_id=1,
        status='Aguardando pagamento',
        canal_pedido='Toten',
        valor_pedido=10.50,
    )
    session.add(new_pedido)
    session.commit()
    pedido = session.scalar(select(Pedido).where(Pedido.pedido_id == 1))
    assert pedido.pedido_id == 1


def test_create_pagamento(session):
    new_pagamento = Pagamento(
        pedido_id=1,
        status='aprovado',
        metodo='cartão',
    )
    session.add(new_pagamento)
    session.commit()
    pagamento = session.scalar(
        select(Pagamento).where(Pagamento.pedido_id == 1)
    )
    assert pagamento.pedido_id == 1


def test_create_item_pedido(session):
    new_item_pedido = ItemPedido(
        pedido_id=1,
        produto_id=1,
        quantidade=10,
        preco_unitario=10.50,
    )
    session.add(new_item_pedido)
    session.commit()
    item_pedido = session.scalar(
        select(ItemPedido).where(ItemPedido.pedido_id == 1)
    )
    assert item_pedido.pedido_id == 1
