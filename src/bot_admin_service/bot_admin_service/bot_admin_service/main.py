from uuid import uuid4

from aiogram.types import Update
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.middleware import is_valid_uuid4
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from bot_admin_service._logging import configure_logging
from bot_admin_service.api.api_v1.api import api_router
from bot_admin_service.bot.dispatcher import dp
from bot_admin_service.bot.loader import main_bot
from bot_admin_service.bot.main import startup_bot, shutdown_bot
from bot_admin_service.core.config import get_app_settings
from bot_admin_service.db.session import engine, get_db
from bot_admin_service.db.utils import create_database

configure_logging()

logger.warning(
    f"USE_RBAC={get_app_settings().USE_RBAC},"
    f" USE_USER_CHECKS={get_app_settings().USE_USER_CHECKS},"
    f" USE_EMAILS={get_app_settings().USE_EMAILS}"
    f" PROFILE_QUERY_MODE={get_app_settings().SQLALCHEMY_PROFILE_QUERY_MODE}"
)


def get_application() -> FastAPI:
    application = FastAPI(**get_app_settings().fastapi_kwargs)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=get_app_settings().APP_BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        expose_headers=["*"],
    )
    application.include_router(
        api_router, prefix=get_app_settings().api_prefix
    )
    # application.middleware("http")(LoguruLoggingMiddleware())
    application.add_middleware(
        CorrelationIdMiddleware,
        header_name="X-Request-ID",
        update_request_header=True,
        generator=lambda: uuid4().hex,
        validator=is_valid_uuid4,
        transformer=lambda a: a,
    )
    return application


app = get_application()


@app.on_event("startup")
async def startup():
    async with get_db() as db:
        await create_database(db)
    await startup_bot(dp)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
    await shutdown_bot(dp)


@app.post(get_app_settings().webhook_path)
async def bot_webhook(update: dict):
    telegram_update = Update(**update)
    await dp.feed_update(bot=main_bot, update=telegram_update)
