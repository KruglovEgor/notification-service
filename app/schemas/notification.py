from enum import Enum

from pydantic import BaseModel, Field


class NotificationType(str, Enum):
    email = "email"
    telegram = "telegram"


class NotificationCreate(BaseModel):
    user_id: int = Field(..., description="User identifier", examples=[123])
    message: str = Field(
        ..., description="Notification message", examples=["Your code: 1111"]
    )
    type: NotificationType = Field(
        ..., description="Notification type", examples=["telegram"]
    )


class NotificationOut(BaseModel):
    id: int = Field(..., description="Notification id", examples=[1])
    user_id: int = Field(..., description="User identifier", examples=[123])
    message: str = Field(
        ..., description="Notification message", examples=["Your code: 1111"]
    )
    type: NotificationType = Field(
        ..., description="Notification type", examples=["telegram"]
    )
    status: str = Field(..., description="Notification status", examples=["pending"])
