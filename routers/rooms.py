from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import provide_current_user, provide_session
from schemas.rooms import RoomCreatePayload, RoomListParams, RoomRecord, RoomUpdatePayload
from services.rooms import create_room, delete_room, get_room, list_rooms, update_room


rooms_router = APIRouter(prefix="/rooms", tags=["Rooms"], dependencies=[Depends(provide_current_user)])


@rooms_router.get("/", response_model=list[RoomRecord])
async def list_rooms_route(
    params: Annotated[RoomListParams, Depends()],
    session: AsyncSession = Depends(provide_session),
) -> list[RoomRecord]:
    return await list_rooms(session=session, params=params)


@rooms_router.post("/", response_model=RoomRecord, status_code=status.HTTP_201_CREATED)
async def create_room_route(
    payload: RoomCreatePayload,
    session: AsyncSession = Depends(provide_session),
) -> RoomRecord:
    return await create_room(session=session, payload=payload)


@rooms_router.get("/{room_id}", response_model=RoomRecord)
async def get_room_route(
    room_id: UUID,
    session: AsyncSession = Depends(provide_session),
) -> RoomRecord:
    return await get_room(session=session, room_id=room_id)


@rooms_router.put("/{room_id}", response_model=RoomRecord)
async def update_room_route(
    room_id: UUID,
    payload: RoomUpdatePayload,
    session: AsyncSession = Depends(provide_session),
) -> RoomRecord:
    return await update_room(session=session, room_id=room_id, payload=payload)


@rooms_router.delete("/{room_id}", response_model=RoomRecord)
async def delete_room_route(
    room_id: UUID,
    session: AsyncSession = Depends(provide_session),
) -> RoomRecord:
    return await delete_room(session=session, room_id=room_id)

