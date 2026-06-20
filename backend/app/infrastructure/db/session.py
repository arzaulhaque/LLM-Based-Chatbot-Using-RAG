from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def get_connect_args(database_url: str) -> dict[str, bool] | None:
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return None


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args=get_connect_args(settings.SQLALCHEMY_DATABASE_URL) or {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
