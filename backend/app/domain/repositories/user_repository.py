from abc import ABC, abstractmethod

from app.infrastructure.db.models.user import UserModel


class UserRepository(ABC):
    @abstractmethod
    def create(self, *, email: str, full_name: str, password_hash: str) -> UserModel:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> UserModel | None:
        raise NotImplementedError
