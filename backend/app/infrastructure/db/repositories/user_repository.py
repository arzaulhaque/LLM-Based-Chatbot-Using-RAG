from sqlalchemy.orm import Session

from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.db.models.user import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, *, email: str, full_name: str, password_hash: str) -> UserModel:
        db_user = UserModel(email=email, full_name=full_name, password_hash=password_hash)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_email(self, email: str) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.email == email).first()
