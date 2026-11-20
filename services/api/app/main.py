from typing import Any, cast

from fastapi import FastAPI

from app.core.config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the API application after validating required runtime settings."""
    runtime_settings = settings if settings is not None else Settings(**cast(Any, {}))

    application = FastAPI(
        title="DPDP360 API",
        version="0.1.0",
        docs_url="/docs" if runtime_settings.app_env != "production" else None,
        redoc_url=None,
        openapi_url="/openapi.json" if runtime_settings.app_env != "production" else None,
    )

    @application.get("/health/live", tags=["health"])
    async def liveness() -> dict[str, str]:
        return {"status": "ok"}

    return application
