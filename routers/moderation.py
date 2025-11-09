from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import provide_session, provide_user_with_roles
from core.enums import UserRole
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
from services.moderation import (
    create_application_history,
    create_event_moderation_history,
    delete_application_history,
    delete_event_moderation_history,
    get_application_history,
    get_event_moderation_history,
    list_application_history,
    list_event_moderation_history,
    update_application_history,
    update_event_moderation_history,
)


moderation_router = APIRouter(
    prefix="/moderation",
    tags=["Moderation"],
    dependencies=[Depends(provide_user_with_roles({UserRole.ADMIN, UserRole.CURATOR}))],
)


@moderation_router.get("/event-history", response_model=list[EventModerationHistoryRecord])
async def list_event_moderation_history_route(
    params: Annotated[EventModerationHistoryListParams, Depends()],
    session: AsyncSession = Depends(provide_session),
) -> list[EventModerationHistoryRecord]:
    return await list_event_moderation_history(session=session, params=params)


@moderation_router.post(
    "/event-history",
    response_model=EventModerationHistoryRecord,
    status_code=status.HTTP_201_CREATED,
)
async def create_event_moderation_history_route(
    payload: EventModerationHistoryCreatePayload,
    session: AsyncSession = Depends(provide_session),
) -> EventModerationHistoryRecord:
    return await create_event_moderation_history(session=session, payload=payload)


@moderation_router.get("/event-history/{history_id}", response_model=EventModerationHistoryRecord)
async def get_event_moderation_history_route(
    history_id: UUID,
    session: AsyncSession = Depends(provide_session),
) -> EventModerationHistoryRecord:
    return await get_event_moderation_history(session=session, history_id=history_id)


@moderation_router.put("/event-history/{history_id}", response_model=EventModerationHistoryRecord)
async def update_event_moderation_history_route(
    history_id: UUID,
    payload: EventModerationHistoryUpdatePayload,
    session: AsyncSession = Depends(provide_session),
) -> EventModerationHistoryRecord:
    return await update_event_moderation_history(
        session=session,
        history_id=history_id,
        payload=payload,
    )


@moderation_router.delete("/event-history/{history_id}", response_model=EventModerationHistoryRecord)
async def delete_event_moderation_history_route(
    history_id: UUID,
    session: AsyncSession = Depends(provide_session),
) -> EventModerationHistoryRecord:
    return await delete_event_moderation_history(session=session, history_id=history_id)


@moderation_router.get("/application-history", response_model=list[ApplicationHistoryRecord])
async def list_application_history_route(
    params: Annotated[ApplicationHistoryListParams, Depends()],
    session: AsyncSession = Depends(provide_session),
) -> list[ApplicationHistoryRecord]:
    return await list_application_history(session=session, params=params)


@moderation_router.post(
    "/application-history",
    response_model=ApplicationHistoryRecord,
    status_code=status.HTTP_201_CREATED,
)
async def create_application_history_route(
    payload: ApplicationHistoryCreatePayload,
    session: AsyncSession = Depends(provide_session),
) -> ApplicationHistoryRecord:
    return await create_application_history(session=session, payload=payload)


@moderation_router.get("/application-history/{history_id}", response_model=ApplicationHistoryRecord)
async def get_application_history_route(
    history_id: UUID,
    session: AsyncSession = Depends(provide_session),
) -> ApplicationHistoryRecord:
    return await get_application_history(session=session, history_id=history_id)


@moderation_router.put("/application-history/{history_id}", response_model=ApplicationHistoryRecord)
async def update_application_history_route(
    history_id: UUID,
    payload: ApplicationHistoryUpdatePayload,
    session: AsyncSession = Depends(provide_session),
) -> ApplicationHistoryRecord:
    return await update_application_history(
        session=session,
        history_id=history_id,
        payload=payload,
    )


@moderation_router.delete("/application-history/{history_id}", response_model=ApplicationHistoryRecord)
async def delete_application_history_route(
    history_id: UUID,
    session: AsyncSession = Depends(provide_session),
) -> ApplicationHistoryRecord:
    return await delete_application_history(session=session, history_id=history_id)

