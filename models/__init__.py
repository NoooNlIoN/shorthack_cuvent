"""
Модели данных для системы Univent
"""

from core.table import Base

# User models
from models.user import User, UserProfile

# Room models
from models.room import Room

# Event models
from models.event import (
    Event,
    EventCategory,
    EventCategoryMapping,
    EventRegistration,
    EventApplication,
)

# Moderation models
from models.moderation import (
    EventModerationHistory,
    ApplicationHistory,
)

# Notification models
from models.notification import Notification


__all__ = [
    "Base",
    # User
    "User",
    "UserProfile",
    # Room
    "Room",
    # Event
    "Event",
    "EventCategory",
    "EventCategoryMapping",
    "EventRegistration",
    "EventApplication",
    # Moderation
    "EventModerationHistory",
    "ApplicationHistory",
    # Notification
    "Notification",
]

