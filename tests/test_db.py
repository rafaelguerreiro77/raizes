from sqlalchemy import select

from raizes.models import Pedido, Usuario


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
