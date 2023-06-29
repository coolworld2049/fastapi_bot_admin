from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import User, Message, CallbackQuery

from bot_admin_service.bot.callbacks import MenuCallback
from bot_admin_service.bot.keyboards.menu import menu_keyboard_builder
from bot_admin_service.bot.keyboards.navigation import menu_navigation_keyboard_builder
from bot_admin_service.bot.loader import main_bot

router = Router(name=__file__)


async def start_cmd(user: User, state: FSMContext, message_id: int):
    with suppress(TelegramBadRequest):
        await main_bot.delete_message(user.id, message_id - 1)
    await state.clear()
    await main_bot.send_message(
        user.id,
        "start",
        reply_markup=menu_keyboard_builder().as_markup(),
    )


@router.message(Command("start"))
async def start_message(message: Message, state: FSMContext):
    await start_cmd(message.from_user, state, message.message_id)


@router.callback_query(MenuCallback.filter(F.name == "start"))
async def start_callback(
    query: CallbackQuery,
    state: FSMContext,
):
    with suppress(TelegramBadRequest):
        await query.message.delete()
    await start_cmd(query.from_user, state, query.message.message_id)


@router.callback_query(MenuCallback.filter(F.name == "help"))
async def help_callback(query: CallbackQuery, state: FSMContext):
    with suppress(TelegramBadRequest):
        await query.message.delete()
    builder = menu_navigation_keyboard_builder(
        menu_callback=MenuCallback(name="start").pack()
    )
    await main_bot.send_message(
        query.from_user.id,
        "help",
        reply_markup=builder.as_markup(),
    )
