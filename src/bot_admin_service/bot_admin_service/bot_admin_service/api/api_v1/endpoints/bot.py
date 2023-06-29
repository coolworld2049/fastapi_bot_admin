from aiogram.types import Update
from fastapi import APIRouter

from bot_admin_service.bot.dispatcher import dp
from bot_admin_service.bot.loader import main_bot
from bot_admin_service.core.config import get_app_settings

router = APIRouter()


@router.post(get_app_settings().webhook_path)
async def bot_webhook(update: dict):
    telegram_update = Update(**update)
    await dp.feed_update(bot=main_bot, update=telegram_update)
