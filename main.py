




from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from routers import (
    auth_router,
    events_router,
    moderation_router,
    notifications_router,
    rooms_router,
    users_router,
)
from services.exceptions import (
    EntityConflictError,
    EntityNotFoundError,
    InvalidStateError,
    ServiceError,
)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi() -> dict:
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title="back-short-hack",
        version="1.0.0",
        routes=app.routes,
    )
    security_schemes = schema.setdefault("components", {}).setdefault("securitySchemes", {})
    security_schemes["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    unsecured_paths = {"/auth/login", "/auth/register", "/auth/refresh"}
    for path, operations in schema.get("paths", {}).items():
        if path in unsecured_paths:
            continue
        for operation in operations.values():
            if isinstance(operation, dict):
                operation.setdefault("security", []).append({"bearerAuth": []})
    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.exception_handler(ServiceError)
async def service_error_handler(_: Request, exc: ServiceError) -> JSONResponse:
    status_code = status.HTTP_400_BAD_REQUEST
    if isinstance(exc, EntityNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, EntityConflictError):
        status_code = status.HTTP_409_CONFLICT
    elif isinstance(exc, InvalidStateError):
        status_code = status.HTTP_400_BAD_REQUEST
    return JSONResponse(
        content={"detail": exc.detail},
        status_code=status_code,
    )


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(events_router)
app.include_router(moderation_router)
app.include_router(notifications_router)
