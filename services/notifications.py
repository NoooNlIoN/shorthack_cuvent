from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.event import Event
from models.notification import Notification
from models.user import User
from schemas.notifications import (
    NotificationCreatePayload,
    NotificationListParams,
    NotificationRecord,
    NotificationUpdatePayload,
)
from services.utils import load_entity


async def create_notification(
    *,
    session: AsyncSession,
    payload: NotificationCreatePayload,
) -> NotificationRecord:
    await load_entity(session=session, model=User, entity_id=payload.user_id, entity_label="User")
    if payload.related_event_id is not None:
        await load_entity(
            session=session,
            model=Event,
            entity_id=payload.related_event_id,
            entity_label="Event",
        )
    notification = Notification(
        user_id=payload.user_id,
        type=payload.type,
        title=payload.title,
        message=payload.message,
        is_read=payload.is_read,
        related_event_id=payload.related_event_id,
    )
    session.add(notification)
    await session.commit()
    await session.refresh(notification)
    return NotificationRecord.model_validate(notification)


async def list_notifications(
    *,
    session: AsyncSession,
    params: NotificationListParams,
) -> list[NotificationRecord]:
    query = select(Notification)
    if params.user_id is not None:
        query = query.where(Notification.user_id == params.user_id)
    if params.type is not None:
        query = query.where(Notification.type == params.type)
    if params.is_read is not None:
        query = query.where(Notification.is_read == params.is_read)
    query = query.offset(params.offset).limit(params.limit)
    result = await session.scalars(query)
    return [NotificationRecord.model_validate(item) for item in result]


async def get_notification(*, session: AsyncSession, notification_id: UUID) -> NotificationRecord:
    notification = await load_entity(
        session=session,
        model=Notification,
        entity_id=notification_id,
        entity_label="Notification",
    )
    return NotificationRecord.model_validate(notification)


async def update_notification(
    *,
    session: AsyncSession,
    notification_id: UUID,
    payload: NotificationUpdatePayload,
) -> NotificationRecord:
    notification = await load_entity(
        session=session,
        model=Notification,
        entity_id=notification_id,
        entity_label="Notification",
    )
    update_data = payload.model_dump(exclude_unset=True)
    if "related_event_id" in update_data and update_data["related_event_id"] is not None:
        await load_entity(
            session=session,
            model=Event,
            entity_id=update_data["related_event_id"],
            entity_label="Event",
        )
    for attribute, value in update_data.items():
        setattr(notification, attribute, value)
    await session.commit()
    await session.refresh(notification)
    return NotificationRecord.model_validate(notification)


async def delete_notification(*, session: AsyncSession, notification_id: UUID) -> NotificationRecord:
    notification = await load_entity(
        session=session,
        model=Notification,
        entity_id=notification_id,
        entity_label="Notification",
    )
    record = NotificationRecord.model_validate(notification)
    await session.delete(notification)
    await session.commit()
    return record

