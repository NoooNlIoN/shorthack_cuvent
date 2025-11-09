from typing import TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.table import Base
from services.exceptions import EntityNotFoundError


ModelType = TypeVar("ModelType", bound=Base)


async def load_entity(
    *,
    session: AsyncSession,
    model: type[ModelType],
    entity_id: UUID,
    entity_label: str | None = None,
) -> ModelType:
    instance = await session.get(model, entity_id)
    if instance is None:
        label = entity_label or model.__name__
        raise EntityNotFoundError(label)
    return instance


async def list_entities(
    *,
    session: AsyncSession,
    model: type[ModelType],
    offset: int,
    limit: int,
) -> list[ModelType]:
    result = await session.scalars(select(model).offset(offset).limit(limit))
    return list(result)

