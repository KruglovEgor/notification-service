from __future__ import annotations

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification


class NotificationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: int, message: str, type: str) -> Notification:
        notification = Notification(
            user_id=user_id,
            message=message,
            type=type,
            status="pending",
            attempts=0,
        )
        self._session.add(notification)
        await self._session.commit()
        await self._session.refresh(notification)
        return notification

    async def list_by_user(self, user_id: int, status: str | None = None) -> list[Notification]:
        stmt = select(Notification).where(Notification.user_id == user_id)
        if status is not None:
            stmt = stmt.where(Notification.status == status)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def update_status(self, notification_id: int, status: str, attempts: int) -> None:
        stmt = (
            update(Notification)
            .where(Notification.id == notification_id)
            .values(status=status, attempts=attempts)
        )
        await self._session.execute(stmt)
        await self._session.commit()
