from fastapi import HTTPException, status

from app.core.security import create_access_token, verify_password
from app.domain.repositories.user_repository import UserRepository
from app.schemas.auth import AuthToken, LoginRequest

# Used when a user is missing to keep password verification timing consistent.
DUMMY_PASSWORD_HASH = "$2b$12$C6UzMDM.H6dfI/f/IKcEeO9Kf2kD4R5nCTpuj/zy4C+OGpamoQ9G2"


class LoginUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, payload: LoginRequest) -> AuthToken:
        user = self.repository.get_by_email(payload.email)
        password_hash = user.password_hash if user else DUMMY_PASSWORD_HASH
        password_valid = verify_password(payload.password, password_hash)
        if user is None or not password_valid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        return AuthToken(access_token=create_access_token(subject=user.email))
