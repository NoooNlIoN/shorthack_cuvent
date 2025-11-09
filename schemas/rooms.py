import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RoomCreatePayload(BaseModel):
    name: str
    capacity: int
    location: str | None = None
    equipment: dict[str, Any] | None = None
    is_available: bool = True


class RoomUpdatePayload(BaseModel):
    name: str | None = None
    capacity: int | None = None
    location: str | None = None
    equipment: dict[str, Any] | None = None
    is_available: bool | None = None


class RoomListParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=500)
    is_available: bool | None = None


class RoomRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    capacity: int
    location: str | None
    equipment: dict[str, Any] | None
    is_available: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime | None

