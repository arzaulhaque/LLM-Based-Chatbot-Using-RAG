from pydantic import BaseModel, EmailStr, Field


class RegisterUserDTO(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class LoginUserDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
