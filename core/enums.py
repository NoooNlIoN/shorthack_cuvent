import enum


class EventStatus(str, enum.Enum):
    """Статус мероприятия"""
    DRAFT = "draft"  # Черновик
    PENDING = "pending"  # На модерации
    APPROVED = "approved"  # Одобрено
    REJECTED = "rejected"  # Отклонено
    CANCELLED = "cancelled"  # Отменено
    COMPLETED = "completed"  # Завершено


class EventType(str, enum.Enum):
    """Тип мероприятия"""
    STUDENT = "student"  # Студенческое
    OFFICIAL = "official"  # Официальное


class UserRole(str, enum.Enum):
    """Роль пользователя"""
    ADMIN = "admin"  # Администратор
    CURATOR = "curator"  # Куратор
    STUDENT = "student"  # Студент


class ApplicationStatus(str, enum.Enum):
    """Статус заявки на участие"""
    PENDING = "pending"  # Ожидает рассмотрения
    APPROVED = "approved"  # Одобрена
    REJECTED = "rejected"  # Отклонена


class ModerationAction(str, enum.Enum):
    """Действие модератора"""
    SUBMIT = "submit"  # Отправлено на модерацию
    APPROVE = "approve"  # Одобрено
    REJECT = "reject"  # Отклонено
    REQUEST_CHANGES = "request_changes"  # Запрошены изменения


class NotificationType(str, enum.Enum):
    """Тип уведомления"""
    APPLICATION_STATUS = "application_status"  # Статус заявки
    EVENT_REMINDER = "event_reminder"  # Напоминание о событии
    NEW_EVENT = "new_event"  # Новое событие
    SYSTEM = "system"  # Системное уведомление

