from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title="Notification Service", version="0.1.0")
app.state.settings = settings


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    return {"status": "ok"}
