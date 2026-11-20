import asyncio

import httpx
import pytest

from app.core.config import Settings
from app.main import create_app
from fastapi import FastAPI
from pydantic import ValidationError


def _valid_settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "_env_file": None,
        "app_env": "test",
        "database_url": "postgresql://test:test@localhost:5432/dpdp360",
        "app_secret_key": "t" * 32,
    }
    values.update(overrides)
    return Settings(**values)


def _get(app: FastAPI, path: str) -> httpx.Response:
    async def request() -> httpx.Response:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            return await client.get(path)

    return asyncio.run(request())


def test_liveness_endpoint_returns_healthy_status() -> None:
    response = _get(create_app(settings=_valid_settings()), "/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_app_creation_rejects_missing_required_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("APP_SECRET_KEY", raising=False)

    with pytest.raises(ValidationError):
        create_app()


def test_production_disables_interactive_api_documentation() -> None:
    application = create_app(settings=_valid_settings(app_env="production"))

    assert application.docs_url is None
    assert application.redoc_url is None
    assert application.openapi_url is None
