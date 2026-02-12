import asyncio
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.core.config import get_settings
from app.core.database import create_engine, create_sessionmaker
from app.core.logging import setup_logging
from app.core.migrations import run_migrations
from app.routers.notifications import router as notifications_router
from app.services import NotificationSender

settings = get_settings()
setup_logging(settings.log_level)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(run_migrations, app.state.settings.database_url)
    yield
    await app.state.db_engine.dispose()


app = FastAPI(title="Notification Service", version="0.1.0", lifespan=lifespan)
app.state.settings = settings
app.state.db_engine = create_engine(settings.database_url)
app.state.db_sessionmaker = create_sessionmaker(app.state.db_engine)
app.state.notification_sender = NotificationSender(app.state.db_sessionmaker)

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
