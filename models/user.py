from uuid import UUID
from typing import Optional

from sqlalchemy import String, Enum as SQLEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from core.table import Base
from core.enums import UserRole


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), nullable=False, default=UserRole.STUDENT)
    telegram_username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    telegram_chat_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    profile: Mapped[Optional["UserProfile"]] = relationship("UserProfile", back_populates="user", uselist=False)
    created_events: Mapped[list["Event"]] = relationship("Event", back_populates="creator", foreign_keys="Event.creator_id")
    curated_events: Mapped[list["Event"]] = relationship("Event", back_populates="curator", foreign_keys="Event.curator_id")
    event_registrations: Mapped[list["EventRegistration"]] = relationship("EventRegistration", back_populates="user")
    event_applications: Mapped[list["EventApplication"]] = relationship("EventApplication", back_populates="applicant")
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, login={self.login}, role={self.role})>"


class UserProfile(Base):
    """Профиль пользователя"""
    __tablename__ = "user_profiles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    faculty: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    study_group: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    interests: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    notification_preferences: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="profile")

    def __repr__(self) -> str:
        return f"<UserProfile(user_id={self.user_id}, faculty={self.faculty})>"

