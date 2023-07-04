from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import User, Message, CallbackQuery
from loguru import logger
from sqlalchemy.exc import IntegrityError

import bot_admin_service.crud as crud
import bot_admin_service.schemas as schemas
from bot_admin_service.bot.callbacks import MenuCallback
from bot_admin_service.db.session import get_db

router = Router(name=__file__)


async def start_cmd(user: User, state: FSMContext):
    try:
        async with get_db() as db:
            bot_user = await crud.bot_user.create(
                db, obj_in=schemas.BotUserUpdate(**user.dict())
            )
        logger.info(f"{user.id} created")
    except IntegrityError as ie:
        logger.info(f"{user.id} already exist")
    await state.clear()


@router.message(Command("start"))
async def start_message(message: Message, state: FSMContext):
    await start_cmd(message.from_user, state)


@router.callback_query(MenuCallback.filter(F.name == "start"))
async def start_callback(
    query: CallbackQuery,
    state: FSMContext,
):
    with suppress(TelegramBadRequest):
        await query.message.delete()
    await start_cmd(query.from_user, state)
