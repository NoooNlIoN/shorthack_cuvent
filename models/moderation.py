from uuid import UUID
from typing import Optional

from sqlalchemy import String, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.table import Base
from core.enums import ModerationAction


class EventModerationHistory(Base):
    """История модерации мероприятия кураторами"""
    __tablename__ = "event_moderation_history"

    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    curator_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action: Mapped[ModerationAction] = mapped_column(SQLEnum(ModerationAction), nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    event: Mapped["Event"] = relationship("Event", back_populates="moderation_history")
    curator: Mapped["User"] = relationship("User", foreign_keys=[curator_id])

    def __repr__(self) -> str:
        return f"<EventModerationHistory(id={self.id}, event_id={self.event_id}, action={self.action})>"


class ApplicationHistory(Base):
    """История модерации заявок на участие"""
    __tablename__ = "application_history"

    application_id: Mapped[UUID] = mapped_column(ForeignKey("event_applications.id", ondelete="CASCADE"), nullable=False, index=True)
    moderator_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action: Mapped[ModerationAction] = mapped_column(SQLEnum(ModerationAction), nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    application: Mapped["EventApplication"] = relationship("EventApplication", back_populates="history")
    moderator: Mapped["User"] = relationship("User", foreign_keys=[moderator_id])

    def __repr__(self) -> str:
        return f"<ApplicationHistory(id={self.id}, application_id={self.application_id}, action={self.action})>"

