from typing import Optional

from sqlalchemy import String, Integer, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.table import Base


class Room(Base):
    """Модель аудитории"""
    __tablename__ = "rooms"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    equipment: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    events: Mapped[list["Event"]] = relationship("Event", back_populates="room")

    def __repr__(self) -> str:
        return f"<Room(id={self.id}, name={self.name}, capacity={self.capacity})>"

