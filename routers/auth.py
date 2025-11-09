from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import provide_current_user, provide_session
from core.security import create_access_token
from schemas.auth import LoginPayload, RegisterPayload, TokenPayload
from schemas.users import UserRecord
from services.auth import authenticate_user, register_user


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", response_model=TokenPayload)
async def login_route(
    payload: LoginPayload,
    session: AsyncSession = Depends(provide_session),
) -> TokenPayload:
    return await authenticate_user(session=session, payload=payload)


@auth_router.post("/register", response_model=UserRecord, status_code=status.HTTP_201_CREATED)
async def register_route(
    payload: RegisterPayload,
    session: AsyncSession = Depends(provide_session),
) -> UserRecord:
    return await register_user(session=session, payload=payload)


@auth_router.get("/me", response_model=UserRecord)
async def get_current_user_route(
    current_user: UserRecord = Depends(provide_current_user),
) -> UserRecord:
    return current_user


@auth_router.post("/refresh", response_model=TokenPayload)
async def refresh_token_route(
    current_user: UserRecord = Depends(provide_current_user),
) -> TokenPayload:
    token = create_access_token({"sub": str(current_user.id)})
    return TokenPayload(access_token=token, user_id=current_user.id)

