from fastapi import HTTPException, status

from app.core.security import create_access_token, verify_password
from app.domain.repositories.user_repository import UserRepository
from app.schemas.auth import AuthToken, LoginRequest


class LoginUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, payload: LoginRequest) -> AuthToken:
        user = self.repository.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        return AuthToken(access_token=create_access_token(subject=user.email))
