from uuid import UUID

from pydantic import BaseModel

from core.enums import UserRole


class LoginPayload(BaseModel):
    login: str
    password: str


class TokenPayload(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: UUID


class RegisterPayload(BaseModel):
    login: str
    password: str
    role: UserRole = UserRole.STUDENT
    telegram_username: str | None = None
    telegram_chat_id: str | None = None

