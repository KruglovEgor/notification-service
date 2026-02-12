from __future__ import annotations

import asyncio
import random

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.schemas.notification import NotificationType
from app.services.notification_service import NotificationService
from app.storage.notification_repository import NotificationRepository


class NotificationSender:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = sessionmaker

    async def send(self, notification_id: int, notification_type: NotificationType) -> None:
        delay = 1.0 if notification_type == NotificationType.email else 0.2
        await asyncio.sleep(delay)

        for attempt in range(1, 4):
            failed = self._should_fail()
            async with self._sessionmaker() as session:
                service = NotificationService(NotificationRepository(session))
                if failed and attempt < 3:
                    await asyncio.sleep(10 * attempt)
                    continue
                if failed:
                    await service.update_status(notification_id, "failed", attempt)
                    return
                await service.update_status(notification_id, "sent", attempt)
                return

    def _should_fail(self) -> bool:
        return random.random() < 0.1
