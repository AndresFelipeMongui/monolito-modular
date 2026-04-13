import os
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///./test.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

class Base(DeclarativeBase):
    pass

def get_db() -> Generator[Session, None, None]:
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()