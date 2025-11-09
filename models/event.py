import datetime
from uuid import UUID
from typing import Optional

from sqlalchemy import String, Text, DateTime, Integer, Boolean, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.table import Base
from core.enums import EventStatus, EventType


class Event(Base):
    """Модель мероприятия"""
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    event_date: Mapped[datetime.date] = mapped_column(nullable=False, index=True)
    start_time: Mapped[datetime.time] = mapped_column(nullable=False)
    end_time: Mapped[datetime.time] = mapped_column(nullable=False)
    
    # Участники
    registered_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_participants: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Статусы
    status: Mapped[EventStatus] = mapped_column(SQLEnum(EventStatus), default=EventStatus.DRAFT, nullable=False, index=True)
    event_type: Mapped[EventType] = mapped_column(SQLEnum(EventType), default=EventType.STUDENT, nullable=False, index=True)
    
    # Создатель и локация
    creator_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    curator_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    is_external_venue: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    room_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True)
    external_location: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Модерация участников
    need_approve_candidates: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    creator: Mapped["User"] = relationship("User", back_populates="created_events", foreign_keys=[creator_id])
    curator: Mapped["User"] = relationship("User", back_populates="curated_events", foreign_keys=[curator_id])
    room: Mapped[Optional["Room"]] = relationship("Room", back_populates="events")
    categories: Mapped[list["EventCategoryMapping"]] = relationship("EventCategoryMapping", back_populates="event", cascade="all, delete-orphan")
    registrations: Mapped[list["EventRegistration"]] = relationship("EventRegistration", back_populates="event", cascade="all, delete-orphan")
    applications: Mapped[list["EventApplication"]] = relationship("EventApplication", back_populates="event", cascade="all, delete-orphan")
    moderation_history: Mapped[list["EventModerationHistory"]] = relationship("EventModerationHistory", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Event(id={self.id}, title={self.title}, status={self.status}, date={self.event_date})>"


class EventCategory(Base):
    """Категория мероприятия"""
    __tablename__ = "event_categories"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationships
    events: Mapped[list["EventCategoryMapping"]] = relationship("EventCategoryMapping", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<EventCategory(id={self.id}, name={self.name})>"


class EventCategoryMapping(Base):
    """Связь мероприятия и категории (many-to-many)"""
    __tablename__ = "event_category_mapping"

    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id: Mapped[UUID] = mapped_column(ForeignKey("event_categories.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relationships
    event: Mapped["Event"] = relationship("Event", back_populates="categories")
    category: Mapped["EventCategory"] = relationship("EventCategory", back_populates="events")

    def __repr__(self) -> str:
        return f"<EventCategoryMapping(event_id={self.event_id}, category_id={self.category_id})>"


class EventRegistration(Base):
    """Регистрация на мероприятие (без модерации)"""
    __tablename__ = "event_registrations"

    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    event: Mapped["Event"] = relationship("Event", back_populates="registrations")
    user: Mapped["User"] = relationship("User", back_populates="event_registrations")

    def __repr__(self) -> str:
        return f"<EventRegistration(event_id={self.event_id}, user_id={self.user_id})>"


class EventApplication(Base):
    """Заявка на участие в мероприятии (с модерацией)"""
    __tablename__ = "event_applications"

    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    applicant_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False, index=True)
    motivation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    event: Mapped["Event"] = relationship("Event", back_populates="applications")
    applicant: Mapped["User"] = relationship("User", back_populates="event_applications")
    history: Mapped[list["ApplicationHistory"]] = relationship("ApplicationHistory", back_populates="application", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<EventApplication(id={self.id}, event_id={self.event_id}, status={self.status})>"

