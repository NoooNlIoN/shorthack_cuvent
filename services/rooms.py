from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.room import Room
from services.exceptions import EntityConflictError, InvalidStateError
from services.utils import load_entity
from schemas.rooms import (
    RoomCreatePayload,
    RoomListParams,
    RoomRecord,
    RoomUpdatePayload,
)


async def create_room(*, session: AsyncSession, payload: RoomCreatePayload) -> RoomRecord:
    if payload.capacity <= 0:
        raise InvalidStateError("capacity must be positive")
    existing_room = await session.scalar(select(Room).where(Room.name == payload.name))
    if existing_room is not None:
        raise EntityConflictError("Room name")
    room = Room(
        name=payload.name,
        capacity=payload.capacity,
        location=payload.location,
        equipment=payload.equipment,
        is_available=payload.is_available,
    )
    session.add(room)
    await session.commit()
    await session.refresh(room)
    return RoomRecord.model_validate(room)


async def list_rooms(*, session: AsyncSession, params: RoomListParams) -> list[RoomRecord]:
    query = select(Room)
    if params.is_available is not None:
        query = query.where(Room.is_available == params.is_available)
    query = query.offset(params.offset).limit(params.limit)
    result = await session.scalars(query)
    return [RoomRecord.model_validate(item) for item in result]


async def get_room(*, session: AsyncSession, room_id: UUID) -> RoomRecord:
    room = await load_entity(session=session, model=Room, entity_id=room_id, entity_label="Room")
    return RoomRecord.model_validate(room)


async def update_room(*, session: AsyncSession, room_id: UUID, payload: RoomUpdatePayload) -> RoomRecord:
    room = await load_entity(session=session, model=Room, entity_id=room_id, entity_label="Room")
    update_data = payload.model_dump(exclude_unset=True)
    if "capacity" in update_data and update_data["capacity"] is not None and update_data["capacity"] <= 0:
        raise InvalidStateError("capacity must be positive")
    if "name" in update_data:
        requested_name = update_data["name"]
        if requested_name is not None:
            room_conflict = await session.scalar(
                select(Room).where(Room.name == requested_name, Room.id != room_id)
            )
            if room_conflict is not None:
                raise EntityConflictError("Room name")
    for attribute, value in update_data.items():
        setattr(room, attribute, value)
    await session.commit()
    await session.refresh(room)
    return RoomRecord.model_validate(room)


async def delete_room(*, session: AsyncSession, room_id: UUID) -> RoomRecord:
    room = await load_entity(session=session, model=Room, entity_id=room_id, entity_label="Room")
    record = RoomRecord.model_validate(room)
    await session.delete(room)
    await session.commit()
    return record

