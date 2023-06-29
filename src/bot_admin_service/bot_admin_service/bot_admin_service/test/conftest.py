import asyncio
from typing import Dict, AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from bot_admin_service.core.config import get_app_settings
from bot_admin_service.db.session import get_db
from bot_admin_service.main import app
from bot_admin_service.test.utils.user import (
    authentication_token_from_email,
    get_superuser_token_headers,
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncGenerator:
    async with AsyncClient(
        app=app,
        base_url=f"http://{get_app_settings().APP_HOST}:{get_app_settings().APP_PORT}",
    ) as _client:
        yield _client


@pytest_asyncio.fixture(scope="session")
async def db() -> AsyncGenerator:
    async with get_db() as s:
        yield s


# noinspection PyShadowingNames
@pytest_asyncio.fixture(scope="module")
async def superuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    return await get_superuser_token_headers(client)


# noinspection PyShadowingNames
@pytest_asyncio.fixture(scope="module")
async def normal_user_token_headers(client: AsyncClient) -> Dict[str, str]:
    return await authentication_token_from_email(
        client=client,
        email=get_app_settings().FIRST_SUPERUSER_EMAIL,
        password=get_app_settings().FIRST_SUPERUSER_PASSWORD,
    )
