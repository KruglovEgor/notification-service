from __future__ import annotations

from app.storage.notification_storage import NotificationRecord, NotificationStorage


class NotificationService:
    def __init__(self, storage: NotificationStorage) -> None:
        self._storage = storage

    def create(self, user_id: int, message: str, type: str) -> NotificationRecord:
        return self._storage.create(user_id=user_id, message=message, type=type)

    def list_by_user(
        self, user_id: int, status: str | None = None
    ) -> list[NotificationRecord]:
        return list(self._storage.list_by_user(user_id=user_id, status=status))

    def update_status(self, notification_id: int, status: str, attempts: int | None = None) -> None:
        self._storage.update_status(notification_id, status, attempts)
