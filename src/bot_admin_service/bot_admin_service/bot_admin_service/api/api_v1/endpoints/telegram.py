import asyncio
from typing import Optional, Literal, Annotated

from aiogram import Bot
from aiogram.types import Update, BufferedInputFile, InputMediaPhoto, InputMediaVideo
from fastapi import APIRouter, Body, Depends, UploadFile
from fastapi.params import Param, File
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from bot_admin_service import crud
from bot_admin_service.api.deps import auth
from bot_admin_service.api.deps.bot import get_main_bot
from bot_admin_service.bot.dispatcher import dp
from bot_admin_service.bot.loader import main_bot
from bot_admin_service.core.config import get_app_settings
from bot_admin_service.db import models
from bot_admin_service.db.dependency import get_session
from bot_admin_service.schemas import RequestParams

router = APIRouter(prefix=f"/bot")


@router.post(get_app_settings().BOT_TOKEN)
async def bot_webhook(update: dict):
    telegram_update = Update(**update)
    await dp.feed_update(bot=main_bot, update=telegram_update)


@router.post(
    f"{get_app_settings().BOT_TOKEN}/post",
)
async def publish_post(
    files: Annotated[list[UploadFile], File(...)] = None,
    text: Optional[str] = Body(..., media_type="text/base"),
    parse_mode: Literal["HTML", "MarkdownV2"] = "HTML",
    disable_web_page_preview: Optional[bool] = None,
    disable_notification: Optional[bool] = None,
    protect_content: Optional[bool] = None,
    delay: Optional[float] = Param(
        0.1, description="delay in seconds between send messages"
    ),
    db: AsyncSession = Depends(get_session),
    bot: Bot = Depends(get_main_bot),
    current_user: models.User = Depends(auth.get_active_current_user),
):
    input_media: list[InputMediaPhoto | InputMediaVideo] = []
    for i, file in enumerate(files):
        media = BufferedInputFile(await file.read(), file.filename)
        if file.content_type.startswith("image"):
            input_media_photo = InputMediaPhoto(
                media=media,
                caption=text if i == 0 else None,
                parse_mode=parse_mode,
            )
            input_media.append(input_media_photo)
        elif file.content_type.startswith("video"):
            input_media_video = InputMediaVideo(
                media=media,
                caption=text if i == 0 else None,
                parse_mode=parse_mode,
            )
            input_media.append(input_media_video)
    users = await crud.bot_user.get_multi(
        db,
        RequestParams(limit=None),
    )
    send_messages_count = 0
    for u in users:
        await asyncio.sleep(delay)
        try:
            if len(input_media) > 0:
                await bot.send_media_group(
                    chat_id=u.id,
                    media=input_media,
                    disable_notification=disable_notification,
                    protect_content=protect_content,
                )
            else:
                await bot.send_message(
                    chat_id=u.id,
                    text=text,
                    parse_mode=parse_mode,
                    disable_web_page_preview=disable_web_page_preview,
                    disable_notification=disable_notification,
                    protect_content=protect_content,
                )
            send_messages_count += 1
        except Exception as e:
            logger.error(e)
            response = JSONResponse(content=str(e.args), status_code=status.HTTP_200_OK)
    return JSONResponse(
        content={
            "users_count": len(users),
            "send_messages_count": send_messages_count,
        },
        status_code=status.HTTP_200_OK,
    )
