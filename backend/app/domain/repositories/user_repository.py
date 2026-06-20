from abc import ABC, abstractmethod

from app.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, *, email: str, full_name: str, password_hash: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError
