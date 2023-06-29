from aiogram import Bot

from bot_admin_service.bot.loader import main_bot


async def get_main_bot() -> Bot:
    return main_bot
