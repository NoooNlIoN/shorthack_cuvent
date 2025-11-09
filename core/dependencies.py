from collections.abc import AsyncIterator, Awaitable, Callable

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from core.enums import UserRole
from services.auth import resolve_current_user
from services.exceptions import InvalidStateError
from schemas.users import UserRecord


async def provide_session() -> AsyncIterator[AsyncSession]:
    async for session in get_session():
        yield session


async def provide_current_user(
    request: Request,
    session: AsyncSession = Depends(provide_session),
) -> UserRecord:
    authorization_header = request.headers.get("authorization")
    if authorization_header is None:
        raise InvalidStateError("Authorization header missing")
    scheme, _, token = authorization_header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise InvalidStateError("Invalid authorization header")
    return await resolve_current_user(session=session, token=token)


def provide_user_with_roles(allowed_roles: set[UserRole]) -> Callable[[], Awaitable[UserRecord]]:
    async def dependency(current_user: UserRecord = Depends(provide_current_user)) -> UserRecord:
        if current_user.role not in allowed_roles:
            raise InvalidStateError("Insufficient permissions")
        return current_user

    return dependency

