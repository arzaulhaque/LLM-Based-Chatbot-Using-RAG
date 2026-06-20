from fastapi import APIRouter, Depends, status

from app.application.use_cases.auth.login_user import LoginUserUseCase
from app.application.use_cases.auth.register_user import RegisterUserUseCase
from app.core.deps import get_current_active_user, get_login_use_case, get_register_use_case
from app.schemas.auth import (
    AuthToken,
    LoginRequest,
    LogoutResponse,
    RegisterRequest,
    UserResponse,
)

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, use_case: RegisterUserUseCase = Depends(get_register_use_case)) -> UserResponse:
    return use_case.execute(payload)


@router.post("/login", response_model=AuthToken)
def login(payload: LoginRequest, use_case: LoginUserUseCase = Depends(get_login_use_case)) -> AuthToken:
    return use_case.execute(payload)


@router.get("/me", response_model=UserResponse)
def me(current_user: UserResponse = Depends(get_current_active_user)) -> UserResponse:
    return current_user


@router.post("/logout", response_model=LogoutResponse)
def logout() -> LogoutResponse:
    return LogoutResponse(message="Logout successful")
