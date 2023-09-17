from sqlmodel import create_engine,SQLModel,Session
from database import models


connected : bool = None
url = f"sqlite:///db.sqlite3?check_same_thread=False"
engine = create_engine(url)


def create_database_and_models():
     SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
