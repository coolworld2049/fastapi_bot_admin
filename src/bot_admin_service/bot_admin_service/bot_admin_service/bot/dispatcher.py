import pathlib

from aiogram import Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

dp = Dispatcher(
    name=pathlib.Path(__file__).name,
)
dp.callback_query.middleware(CallbackAnswerMiddleware())
