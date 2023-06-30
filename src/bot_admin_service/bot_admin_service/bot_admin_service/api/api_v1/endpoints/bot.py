import asyncio
from typing import Optional, Literal, List, Any, Annotated

from aiogram import Bot
from aiogram.types import Update, BufferedInputFile, InputMediaPhoto, InputMediaVideo, Message
from fastapi import APIRouter, Body, Depends, UploadFile
from fastapi.params import Param, File
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, Response

from bot_admin_service import crud, schemas
from bot_admin_service.api.deps import auth, params
from bot_admin_service.api.deps.bot import get_main_bot
from bot_admin_service.bot.dispatcher import dp
from bot_admin_service.bot.loader import main_bot
from bot_admin_service.core.config import get_app_settings
from bot_admin_service.db import models, BotUser
from bot_admin_service.db.dependency import get_session
from bot_admin_service.schemas import RequestParams, MessageCreate

router = APIRouter(prefix=f"/bot")


@router.post(get_app_settings().BOT_TOKEN)
async def bot_webhook(update: dict):
    telegram_update = Update(**update)
    await dp.feed_update(bot=main_bot, update=telegram_update)


@router.get(
    "/users",
    response_model=List[schemas.BotUser],
)
async def read_bot_users(
    response: Response,
    current_user: models.User = Depends(auth.get_active_current_user),
    request_params: RequestParams = Depends(
        params.parse_params(BotUser),
    ),
    db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Retrieve bot users.
    """
    users, total = await crud.bot_user.get_multi(db, request_params)
    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(users)}/{total}"
    return users


@router.get(
    "/users/{id}",
    response_model=schemas.User,
)
async def read_user_by_id(
    id: int,
    db: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(auth.get_active_current_user),
) -> Any:
    """
    Get a specific bot user.
    """
    user = await crud.bot_user.get(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.get(
    "/posts",
    response_model=List[schemas.Message],
)
async def read_messages(
    response: Response,
    current_user: models.User = Depends(auth.get_active_current_user),
    request_params: RequestParams = Depends(
        params.parse_params(models.Message),
    ),
    db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Retrieve users.
    """
    messages, total = await crud.message.get_multi(db, request_params)
    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(messages)}/{total}"
    return messages


@router.post(
    f"/posts",
)
async def publish_post(
    text: Optional[str] = Body(..., media_type="text/base"),
    file: list[UploadFile] | None = None,
    parse_mode: Literal["HTML", "MarkdownV2"] = "HTML",
    disable_web_page_preview: Optional[bool] = None,
    disable_notification: Optional[bool] = None,
    protect_content: Optional[bool] = None,
    delay: Optional[float] = Param(
        0.1, description="delay in seconds between send messages"
    ),
    current_user: models.User = Depends(auth.get_active_current_user),
    db: AsyncSession = Depends(get_session),
    bot: Bot = Depends(get_main_bot),
):
    input_media: list[InputMediaPhoto | InputMediaVideo] = []
    if file:
        for i, f in enumerate(file):
            media = BufferedInputFile(await f.read(), f.filename)
            if f.content_type.startswith("image"):
                input_media_photo = InputMediaPhoto(
                    media=media,
                    caption=text if i == 0 else None,
                    parse_mode=parse_mode,
                )
                input_media.append(input_media_photo)
            elif f.content_type.startswith("video"):
                input_media_video = InputMediaVideo(
                    media=media,
                    caption=text if i == 0 else None,
                    parse_mode=parse_mode,
                )
                input_media.append(input_media_video)
    users, total = await crud.bot_user.get_multi(
        db,
        RequestParams(limit=None),
    )
    send_messages_count = 0
    messages: list[Message] = []
    for u in users:
        await asyncio.sleep(delay)
        try:
            if len(input_media) > 0:
                message = await bot.send_media_group(
                    chat_id=u.id,
                    media=input_media,
                    disable_notification=disable_notification,
                    protect_content=protect_content,
                )
                messages.extend(message)
            else:
                message = await bot.send_message(
                    chat_id=u.id,
                    text=text,
                    parse_mode=parse_mode,
                    disable_web_page_preview=disable_web_page_preview,
                    disable_notification=disable_notification,
                    protect_content=protect_content,
                )
                messages.append(message)
            send_messages_count += 1
        except Exception as e:
            logger.error(e)
            response = JSONResponse(content=str(e.args), status_code=status.HTTP_200_OK)
    if len(messages) > 0:
        for m in messages:
            await crud.message.create(db, obj_in=MessageCreate(id=m.message_id, message=m.json()))
    return JSONResponse(
        content={
            "users_count": len(users),
            "send_messages_count": send_messages_count,
        },
        status_code=status.HTTP_200_OK,
    )
