from pathlib import Path

from sqlmodel import SQLModel, Session, create_engine

from .settings import settings


def _ensure_dirs() -> None:
    Path(settings.db_path).parent.mkdir(parents=True, exist_ok=True)


_ensure_dirs()
engine = create_engine(f"sqlite:///{settings.db_path}", echo=False)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
