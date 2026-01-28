from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class NotificationRecord:
    id: int
    user_id: int
    message: str
    type: str
    status: str
    attempts: int = 0


@dataclass
class NotificationStorage:
    _items: list[NotificationRecord] = field(default_factory=list)
    _next_id: int = 1

    def create(self, user_id: int, message: str, type: str) -> NotificationRecord:
        record = NotificationRecord(
            id=self._next_id,
            user_id=user_id,
            message=message,
            type=type,
            status="pending",
        )
        self._next_id += 1
        self._items.append(record)
        return record

    def list_by_user(self, user_id: int, status: str | None = None) -> Iterable[NotificationRecord]:
        if status is None:
            return [item for item in self._items if item.user_id == user_id]
        return [
            item
            for item in self._items
            if item.user_id == user_id and item.status == status
        ]

    def update_status(self, notification_id: int, status: str, attempts: int | None = None) -> None:
        for item in self._items:
            if item.id == notification_id:
                item.status = status
                if attempts is not None:
                    item.attempts = attempts
                return
