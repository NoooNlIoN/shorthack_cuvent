from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import create_access_token, decode_access_token, hash_password, verify_password
from models.user import User
from services.exceptions import EntityConflictError, EntityNotFoundError, InvalidStateError
from services.utils import load_entity
from schemas.auth import LoginPayload, RegisterPayload, TokenPayload
from schemas.users import UserCreatePayload, UserRecord


async def authenticate_user(*, session: AsyncSession, payload: LoginPayload) -> TokenPayload:
    user = await session.scalar(select(User).where(User.login == payload.login))
    if user is None:
        raise EntityNotFoundError("User")
    if not verify_password(payload.password, user.password_hash):
        raise InvalidStateError("Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return TokenPayload(access_token=token, user_id=user.id)


async def register_user(*, session: AsyncSession, payload: RegisterPayload) -> UserRecord:
    existing_user = await session.scalar(select(User).where(User.login == payload.login))
    if existing_user is not None:
        raise EntityConflictError("User login")
    hashed_password = hash_password(payload.password)
    user_payload = UserCreatePayload(
        login=payload.login,
        password_hash=hashed_password,
        role=payload.role,
        telegram_username=payload.telegram_username,
        telegram_chat_id=payload.telegram_chat_id,
    )
    user = User(
        login=user_payload.login,
        password_hash=user_payload.password_hash,
        role=user_payload.role,
        telegram_username=user_payload.telegram_username,
        telegram_chat_id=user_payload.telegram_chat_id,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserRecord.model_validate(user)


async def resolve_current_user(*, session: AsyncSession, token: str) -> UserRecord:
    payload = decode_access_token(token)
    subject = payload.get("sub")
    if subject is None:
        raise InvalidStateError("Token subject missing")
    try:
        user_id = UUID(subject)
    except ValueError as exc:
        raise InvalidStateError("Invalid token subject") from exc
    user = await load_entity(session=session, model=User, entity_id=user_id, entity_label="User")
    return UserRecord.model_validate(user)

