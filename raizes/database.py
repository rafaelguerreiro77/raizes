from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from raizes.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()