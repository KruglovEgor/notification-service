from fastapi import FastAPI

app = FastAPI(title="Notification Service", version="0.1.0")


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    return {"status": "ok"}
