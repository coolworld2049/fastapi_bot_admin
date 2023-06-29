from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot_admin_service.bot.callbacks import MenuCallback


def menu_keyboard_builder():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Main",
            callback_data=MenuCallback(
                name="main",
            ).pack(),
        ),
        InlineKeyboardButton(
            text="📄 Help",
            callback_data=MenuCallback(
                name="help",
            ).pack(),
        ),
    )
    builder.adjust(2, 2)
    return builder
