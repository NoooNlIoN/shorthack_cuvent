from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.event import Event, EventApplication
from models.moderation import EventModerationHistory, ApplicationHistory
from models.user import User
from schemas.moderation import (
    ApplicationHistoryCreatePayload,
    ApplicationHistoryListParams,
    ApplicationHistoryRecord,
    ApplicationHistoryUpdatePayload,
    EventModerationHistoryCreatePayload,
    EventModerationHistoryListParams,
    EventModerationHistoryRecord,
    EventModerationHistoryUpdatePayload,
)
from services.utils import load_entity


async def create_event_moderation_history(
    *,
    session: AsyncSession,
    payload: EventModerationHistoryCreatePayload,
) -> EventModerationHistoryRecord:
    await load_entity(session=session, model=Event, entity_id=payload.event_id, entity_label="Event")
    await load_entity(session=session, model=User, entity_id=payload.curator_id, entity_label="User")
    history = EventModerationHistory(
        event_id=payload.event_id,
        curator_id=payload.curator_id,
        action=payload.action,
        comment=payload.comment,
    )
    session.add(history)
    await session.commit()
    await session.refresh(history)
    return EventModerationHistoryRecord.model_validate(history)


async def list_event_moderation_history(
    *,
    session: AsyncSession,
    params: EventModerationHistoryListParams,
) -> list[EventModerationHistoryRecord]:
    query = select(EventModerationHistory)
    if params.event_id is not None:
        query = query.where(EventModerationHistory.event_id == params.event_id)
    if params.curator_id is not None:
        query = query.where(EventModerationHistory.curator_id == params.curator_id)
    query = query.offset(params.offset).limit(params.limit)
    result = await session.scalars(query)
    return [EventModerationHistoryRecord.model_validate(item) for item in result]


async def get_event_moderation_history(
    *,
    session: AsyncSession,
    history_id: UUID,
) -> EventModerationHistoryRecord:
    history = await load_entity(
        session=session,
        model=EventModerationHistory,
        entity_id=history_id,
        entity_label="EventModerationHistory",
    )
    return EventModerationHistoryRecord.model_validate(history)


async def update_event_moderation_history(
    *,
    session: AsyncSession,
    history_id: UUID,
    payload: EventModerationHistoryUpdatePayload,
) -> EventModerationHistoryRecord:
    history = await load_entity(
        session=session,
        model=EventModerationHistory,
        entity_id=history_id,
        entity_label="EventModerationHistory",
    )
    update_data = payload.model_dump(exclude_unset=True)
    for attribute, value in update_data.items():
        setattr(history, attribute, value)
    await session.commit()
    await session.refresh(history)
    return EventModerationHistoryRecord.model_validate(history)


async def delete_event_moderation_history(
    *,
    session: AsyncSession,
    history_id: UUID,
) -> EventModerationHistoryRecord:
    history = await load_entity(
        session=session,
        model=EventModerationHistory,
        entity_id=history_id,
        entity_label="EventModerationHistory",
    )
    record = EventModerationHistoryRecord.model_validate(history)
    await session.delete(history)
    await session.commit()
    return record


async def create_application_history(
    *,
    session: AsyncSession,
    payload: ApplicationHistoryCreatePayload,
) -> ApplicationHistoryRecord:
    await load_entity(
        session=session,
        model=EventApplication,
        entity_id=payload.application_id,
        entity_label="EventApplication",
    )
    await load_entity(session=session, model=User, entity_id=payload.moderator_id, entity_label="User")
    history = ApplicationHistory(
        application_id=payload.application_id,
        moderator_id=payload.moderator_id,
        action=payload.action,
        comment=payload.comment,
    )
    session.add(history)
    await session.commit()
    await session.refresh(history)
    return ApplicationHistoryRecord.model_validate(history)


async def list_application_history(
    *,
    session: AsyncSession,
    params: ApplicationHistoryListParams,
) -> list[ApplicationHistoryRecord]:
    query = select(ApplicationHistory)
    if params.application_id is not None:
        query = query.where(ApplicationHistory.application_id == params.application_id)
    if params.moderator_id is not None:
        query = query.where(ApplicationHistory.moderator_id == params.moderator_id)
    query = query.offset(params.offset).limit(params.limit)
    result = await session.scalars(query)
    return [ApplicationHistoryRecord.model_validate(item) for item in result]


async def get_application_history(
    *,
    session: AsyncSession,
    history_id: UUID,
) -> ApplicationHistoryRecord:
    history = await load_entity(
        session=session,
        model=ApplicationHistory,
        entity_id=history_id,
        entity_label="ApplicationHistory",
    )
    return ApplicationHistoryRecord.model_validate(history)


async def update_application_history(
    *,
    session: AsyncSession,
    history_id: UUID,
    payload: ApplicationHistoryUpdatePayload,
) -> ApplicationHistoryRecord:
    history = await load_entity(
        session=session,
        model=ApplicationHistory,
        entity_id=history_id,
        entity_label="ApplicationHistory",
    )
    update_data = payload.model_dump(exclude_unset=True)
    for attribute, value in update_data.items():
        setattr(history, attribute, value)
    await session.commit()
    await session.refresh(history)
    return ApplicationHistoryRecord.model_validate(history)


async def delete_application_history(
    *,
    session: AsyncSession,
    history_id: UUID,
) -> ApplicationHistoryRecord:
    history = await load_entity(
        session=session,
        model=ApplicationHistory,
        entity_id=history_id,
        entity_label="ApplicationHistory",
    )
    record = ApplicationHistoryRecord.model_validate(history)
    await session.delete(history)
    await session.commit()
    return record

