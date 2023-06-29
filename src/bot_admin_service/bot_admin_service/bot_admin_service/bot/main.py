from aiogram import Dispatcher
from aiogram.types import BotCommand
from aredis_om import Migrator
from loguru import logger

from bot_admin_service.bot.dispatcher import dp
from bot_admin_service.bot.handlers import menu
from bot_admin_service.bot.loader import main_bot
from bot_admin_service.core.config import get_app_settings


async def startup_bot(dp: Dispatcher) -> None:
    await main_bot.delete_my_commands()
    await main_bot.set_my_commands(
        commands=[BotCommand(command="start", description="start")]
    )
    await main_bot.delete_webhook(drop_pending_updates=True)
    await main_bot.set_webhook(url=get_app_settings().webhook_url)
    logger.debug(await main_bot.get_webhook_info())
    dp.include_routers(
        menu.router,
    )
    await Migrator().run()


async def shutdown_bot(dp: Dispatcher) -> None:
    await dp.storage.close()
    await main_bot.session.close()


async def start_polling_bot():
    try:
        await startup_bot(dp)
        await dp.start_polling(main_bot, polling_timeout=5)
    finally:
        await shutdown_bot(dp)
