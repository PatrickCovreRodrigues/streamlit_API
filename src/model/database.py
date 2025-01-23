from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import session


from src.settings.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session