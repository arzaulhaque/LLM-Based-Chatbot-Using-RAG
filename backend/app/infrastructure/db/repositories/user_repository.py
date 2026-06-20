from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.db.models.user import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, *, email: str, full_name: str, password_hash: str) -> User:
        db_user = UserModel(email=email, full_name=full_name, password_hash=password_hash)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)

    def get_by_email(self, email: str) -> User | None:
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if db_user is None:
            return None
        return self._to_entity(db_user)

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            full_name=model.full_name,
            password_hash=model.password_hash,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
