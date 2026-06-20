from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.application.use_cases.auth.login_user import LoginUserUseCase
from app.application.use_cases.auth.register_user import RegisterUserUseCase
from app.core.security import decode_access_token
from app.infrastructure.db.repositories.user_repository import SQLAlchemyUserRepository
from app.infrastructure.db.session import get_db
from app.schemas.auth import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_user_repository(db: Session = Depends(get_db)) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)


def get_register_use_case(repository: SQLAlchemyUserRepository = Depends(get_user_repository)) -> RegisterUserUseCase:
    return RegisterUserUseCase(repository)


def get_login_use_case(repository: SQLAlchemyUserRepository = Depends(get_user_repository)) -> LoginUserUseCase:
    return LoginUserUseCase(repository)


def get_current_active_user(
    token: str = Depends(oauth2_scheme), repository: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception
    except ValueError as exc:
        raise credentials_exception from exc

    user = repository.get_by_email(subject)
    if user is None:
        raise credentials_exception

    return UserResponse.model_validate(user)
