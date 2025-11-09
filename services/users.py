from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User, UserProfile
from services.exceptions import EntityConflictError, EntityNotFoundError
from services.utils import load_entity, list_entities
from schemas.users import (
    UserCreatePayload,
    UserListParams,
    UserProfileCreatePayload,
    UserProfileListParams,
    UserProfileRecord,
    UserProfileUpdatePayload,
    UserRecord,
    UserUpdatePayload,
)


async def create_user(*, session: AsyncSession, payload: UserCreatePayload) -> UserRecord:
    existing_user = await session.scalar(select(User).where(User.login == payload.login))
    if existing_user is not None:
        raise EntityConflictError("User login")
    user = User(
        login=payload.login,
        password_hash=payload.password_hash,
        role=payload.role,
        telegram_username=payload.telegram_username,
        telegram_chat_id=payload.telegram_chat_id,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserRecord.model_validate(user)


async def list_users(*, session: AsyncSession, params: UserListParams) -> list[UserRecord]:
    query = select(User)
    if params.role is not None:
        query = query.where(User.role == params.role)
    query = query.offset(params.offset).limit(params.limit)
    result = await session.scalars(query)
    return [UserRecord.model_validate(item) for item in result]


async def get_user(*, session: AsyncSession, user_id: UUID) -> UserRecord:
    user = await load_entity(session=session, model=User, entity_id=user_id, entity_label="User")
    return UserRecord.model_validate(user)


async def update_user(*, session: AsyncSession, user_id: UUID, payload: UserUpdatePayload) -> UserRecord:
    user = await load_entity(session=session, model=User, entity_id=user_id, entity_label="User")
    update_data = payload.model_dump(exclude_unset=True)
    if "login" in update_data:
        requested_login = update_data["login"]
        login_conflict = await session.scalar(
            select(User).where(User.login == requested_login, User.id != user_id)
        )
        if login_conflict is not None:
            raise EntityConflictError("User login")
    for attribute, value in update_data.items():
        setattr(user, attribute, value)
    await session.commit()
    await session.refresh(user)
    return UserRecord.model_validate(user)


async def delete_user(*, session: AsyncSession, user_id: UUID) -> UserRecord:
    user = await load_entity(session=session, model=User, entity_id=user_id, entity_label="User")
    record = UserRecord.model_validate(user)
    await session.delete(user)
    await session.commit()
    return record


async def create_user_profile(
    *,
    session: AsyncSession,
    payload: UserProfileCreatePayload,
) -> UserProfileRecord:
    await load_entity(session=session, model=User, entity_id=payload.user_id, entity_label="User")
    existing_profile = await session.scalar(
        select(UserProfile).where(UserProfile.user_id == payload.user_id)
    )
    if existing_profile is not None:
        raise EntityConflictError("UserProfile")
    profile = UserProfile(
        user_id=payload.user_id,
        faculty=payload.faculty,
        study_group=payload.study_group,
        interests=payload.interests,
        notification_preferences=payload.notification_preferences,
    )
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return UserProfileRecord.model_validate(profile)


async def list_user_profiles(
    *,
    session: AsyncSession,
    params: UserProfileListParams,
) -> list[UserProfileRecord]:
    if params.user_id is not None:
        profile = await session.scalar(
            select(UserProfile).where(UserProfile.user_id == params.user_id)
        )
        if profile is None:
            return []
        return [UserProfileRecord.model_validate(profile)]
    profiles = await list_entities(
        session=session,
        model=UserProfile,
        offset=params.offset,
        limit=params.limit,
    )
    return [UserProfileRecord.model_validate(item) for item in profiles]


async def get_user_profile(*, session: AsyncSession, profile_id: UUID) -> UserProfileRecord:
    profile = await load_entity(
        session=session,
        model=UserProfile,
        entity_id=profile_id,
        entity_label="UserProfile",
    )
    return UserProfileRecord.model_validate(profile)


async def get_user_profile_by_user(
    *,
    session: AsyncSession,
    user_id: UUID,
) -> UserProfileRecord:
    profile = await session.scalar(
        select(UserProfile).where(UserProfile.user_id == user_id)
    )
    if profile is None:
        raise EntityNotFoundError("UserProfile")
    return UserProfileRecord.model_validate(profile)


async def update_user_profile(
    *,
    session: AsyncSession,
    profile_id: UUID,
    payload: UserProfileUpdatePayload,
) -> UserProfileRecord:
    profile = await load_entity(
        session=session,
        model=UserProfile,
        entity_id=profile_id,
        entity_label="UserProfile",
    )
    update_data = payload.model_dump(exclude_unset=True)
    for attribute, value in update_data.items():
        setattr(profile, attribute, value)
    await session.commit()
    await session.refresh(profile)
    return UserProfileRecord.model_validate(profile)


async def delete_user_profile(*, session: AsyncSession, profile_id: UUID) -> UserProfileRecord:
    profile = await load_entity(
        session=session,
        model=UserProfile,
        entity_id=profile_id,
        entity_label="UserProfile",
    )
    record = UserProfileRecord.model_validate(profile)
    await session.delete(profile)
    await session.commit()
    return record

