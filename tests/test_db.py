from sqlalchemy import select

from raizes.models import Usuario


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
