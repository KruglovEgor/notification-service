import logging
import time

from fastapi import FastAPI, Request

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.routers.notifications import router as notifications_router
from app.services import NotificationSender, NotificationService
from app.storage.notification_storage import NotificationStorage

settings = get_settings()
setup_logging(settings.log_level)

app = FastAPI(title="Notification Service", version="0.1.0")
app.state.settings = settings
app.state.notification_storage = NotificationStorage()
app.state.notification_service = NotificationService(app.state.notification_storage)
app.state.notification_sender = NotificationSender(app.state.notification_service)

app.include_router(notifications_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("app.request")
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (time.perf_counter() - start) * 1000
        logger.exception(
            "method=%s path=%s status=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            500,
            duration_ms,
        )
        raise
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "method=%s path=%s status=%s duration_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    return {"status": "ok"}
