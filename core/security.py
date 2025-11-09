import datetime
import hashlib
from typing import Any

import jwt

from core.config import settings
from services.exceptions import InvalidStateError


def hash_password(raw_password: str) -> str:
    return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


def verify_password(raw_password: str, stored_hash: str) -> bool:
    return hash_password(raw_password) == stored_hash


def create_access_token(payload: dict[str, Any]) -> str:
    issued_at = datetime.datetime.utcnow()
    expires_at = issued_at + datetime.timedelta(minutes=settings.jwt_expiration_minutes)
    token_payload = {
        **payload,
        "iat": int(issued_at.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    return jwt.encode(token_payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.ExpiredSignatureError as exc:
        raise InvalidStateError("Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise InvalidStateError("Invalid token") from exc

