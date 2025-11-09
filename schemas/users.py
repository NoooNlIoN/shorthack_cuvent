import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from core.enums import UserRole


class UserCreatePayload(BaseModel):
    login: str
    password_hash: str
    role: UserRole = UserRole.STUDENT
    telegram_username: str | None = None
    telegram_chat_id: str | None = None


class UserUpdatePayload(BaseModel):
    login: str | None = None
    password_hash: str | None = None
    role: UserRole | None = None
    telegram_username: str | None = None
    telegram_chat_id: str | None = None


class UserListParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=500)
    role: UserRole | None = None


class UserRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    login: str
    role: UserRole
    telegram_username: str | None
    telegram_chat_id: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


class UserProfileCreatePayload(BaseModel):
    user_id: UUID
    faculty: str | None = None
    study_group: str | None = None
    interests: dict[str, Any] | None = None
    notification_preferences: dict[str, Any] | None = None


class UserProfileUpdatePayload(BaseModel):
    faculty: str | None = None
    study_group: str | None = None
    interests: dict[str, Any] | None = None
    notification_preferences: dict[str, Any] | None = None


class UserProfileListParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=500)
    user_id: UUID | None = None


class UserProfileRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    faculty: str | None
    study_group: str | None
    interests: dict[str, Any] | None
    notification_preferences: dict[str, Any] | None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None

