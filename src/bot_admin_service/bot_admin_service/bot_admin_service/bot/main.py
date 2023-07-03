import asyncio

from aiogram import Dispatcher
from loguru import logger

from bot_admin_service.bot.dispatcher import dp
from bot_admin_service.bot.handlers import menu
from bot_admin_service.bot.loader import main_bot
from bot_admin_service.core.config import get_app_settings


async def startup_bot(dp: Dispatcher) -> None:
    await asyncio.sleep(3)
    webhook_info = await main_bot.get_webhook_info()
    if get_app_settings().webhook_url != webhook_info.url:
        await main_bot.delete_webhook()
        await main_bot.set_webhook(
            url=get_app_settings().webhook_url,
            drop_pending_updates=True,
            max_connections=30,
        )
    logger.info(await main_bot.get_webhook_info())
    dp.include_routers(
        menu.router,
    )


async def shutdown_bot(dp: Dispatcher) -> None:
    await dp.storage.close()
    await main_bot.session.close()


async def start_polling_bot():
    try:
        await startup_bot(dp)
        await dp.start_polling(main_bot, polling_timeout=5)
    finally:
        await shutdown_bot(dp)
