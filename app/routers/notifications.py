from fastapi import APIRouter, BackgroundTasks, Depends, Query, Request, status

from app.schemas.notification import NotificationCreate, NotificationOut, NotificationType
from app.services import NotificationSender, NotificationService

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


def get_service(request: Request) -> NotificationService:
    return request.app.state.notification_service


def get_sender(request: Request) -> NotificationSender:
    return request.app.state.notification_sender


@router.post("", response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
async def create_notification(
    payload: NotificationCreate,
    background_tasks: BackgroundTasks,
    service: NotificationService = Depends(get_service),
    sender: NotificationSender = Depends(get_sender),
) -> NotificationOut:
    record = service.create(
        user_id=payload.user_id, message=payload.message, type=payload.type.value
    )
    background_tasks.add_task(sender.send, record.id, payload.type)
    return NotificationOut(
        id=record.id,
        user_id=record.user_id,
        message=record.message,
        type=payload.type,
        status=record.status,
    )


@router.get("/{user_id}", response_model=list[NotificationOut])
async def list_notifications(
    user_id: int,
    status: str | None = Query(default=None),
    service: NotificationService = Depends(get_service),
) -> list[NotificationOut]:
    items = service.list_by_user(user_id=user_id, status=status)
    return [
        NotificationOut(
            id=item.id,
            user_id=item.user_id,
            message=item.message,
            type=NotificationType(item.type),
            status=item.status,
        )
        for item in items
    ]
