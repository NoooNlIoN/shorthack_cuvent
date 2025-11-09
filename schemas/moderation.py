import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from core.enums import ModerationAction


class EventModerationHistoryCreatePayload(BaseModel):
    event_id: UUID
    curator_id: UUID
    action: ModerationAction
    comment: str | None = None


class EventModerationHistoryUpdatePayload(BaseModel):
    action: ModerationAction | None = None
    comment: str | None = None


class EventModerationHistoryListParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=500)
    event_id: UUID | None = None
    curator_id: UUID | None = None


class EventModerationHistoryRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    event_id: UUID
    curator_id: UUID
    action: ModerationAction
    comment: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


class ApplicationHistoryCreatePayload(BaseModel):
    application_id: UUID
    moderator_id: UUID
    action: ModerationAction
    comment: str | None = None


class ApplicationHistoryUpdatePayload(BaseModel):
    action: ModerationAction | None = None
    comment: str | None = None


class ApplicationHistoryListParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=500)
    application_id: UUID | None = None
    moderator_id: UUID | None = None


class ApplicationHistoryRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    application_id: UUID
    moderator_id: UUID
    action: ModerationAction
    comment: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None

