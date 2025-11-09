import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import (
    Mapped as SQLAlchemyMapped,
)
from sqlalchemy.orm import (
    mapped_column as sqlalchemy_mapped_column,
)


class Base(DeclarativeBase):
    __name__: str
    __tablename__: str
    id: SQLAlchemyMapped[UUID] = sqlalchemy_mapped_column(
        primary_key=True, default=uuid4
    )
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now(),
        onupdate=func.now()
    )