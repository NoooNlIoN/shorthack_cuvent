import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from core.enums import NotificationType


class NotificationCreatePayload(BaseModel):
    user_id: UUID
    type: NotificationType
    title: str
    message: str
    is_read: bool = False
    related_event_id: UUID | None = None


class NotificationUpdatePayload(BaseModel):
    type: NotificationType | None = None
    title: str | None = None
    message: str | None = None
    is_read: bool | None = None
    related_event_id: UUID | None = None


class NotificationListParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=500)
    user_id: UUID | None = None
    type: NotificationType | None = None
    is_read: bool | None = None


class NotificationRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    type: NotificationType
    title: str
    message: str
    is_read: bool
    related_event_id: UUID | None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None

