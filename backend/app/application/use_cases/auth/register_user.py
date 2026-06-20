from fastapi import HTTPException, status

from app.core.security import get_password_hash
from app.domain.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, UserResponse


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, payload: RegisterRequest) -> UserResponse:
        existing_user = self.repository.get_by_email(payload.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered")

        user = self.repository.create(
            email=payload.email,
            full_name=payload.full_name,
            password_hash=get_password_hash(payload.password),
        )
        return UserResponse.model_validate(user)
