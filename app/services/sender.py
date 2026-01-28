from __future__ import annotations

import asyncio
import random

from app.schemas.notification import NotificationType
from app.services.notification_service import NotificationService


class NotificationSender:
    def __init__(self, service: NotificationService) -> None:
        self._service = service

    async def send(self, notification_id: int, notification_type: NotificationType) -> None:
        delay = 1.0 if notification_type == NotificationType.email else 0.2
        await asyncio.sleep(delay)

        for attempt in range(1, 4):
            failed = self._should_fail()
            if failed and attempt < 3:
                continue
            if failed:
                self._service.update_status(notification_id, "failed", attempt)
                return
            self._service.update_status(notification_id, "sent", attempt)
            return

    def _should_fail(self) -> bool:
        return random.random() < 0.1
