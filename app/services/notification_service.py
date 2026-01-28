from __future__ import annotations

from app.models.notification import Notification
from app.storage.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self, repository: NotificationRepository) -> None:
        self._repository = repository

    async def create(self, user_id: int, message: str, type: str) -> Notification:
        return await self._repository.create(user_id=user_id, message=message, type=type)

    async def list_by_user(
        self, user_id: int, status: str | None = None
    ) -> list[Notification]:
        return await self._repository.list_by_user(user_id=user_id, status=status)

    async def update_status(self, notification_id: int, status: str, attempts: int) -> None:
        await self._repository.update_status(notification_id, status, attempts)
