import os

from aiogram import Bot
from redis.asyncio import Redis

from bot_admin_service.core.config import get_app_settings

os.environ["REDIS_OM_URL"] = get_app_settings().redis_url
redis = Redis.from_url(get_app_settings().redis_url)
main_bot = Bot(get_app_settings().BOT_TOKEN, parse_mode="HTML")
