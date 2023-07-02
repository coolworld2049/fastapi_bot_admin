import asyncio
from typing import List, Any, Optional

from aiogram import Bot
from aiogram.types import (
    InputMediaPhoto,
    InputMediaVideo,
    BufferedInputFile,
    InputMediaDocument,
    InputMediaAudio,
)
from fastapi import Depends, APIRouter
from fastapi.params import Param
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from bot_admin_service import schemas, crud
from bot_admin_service.api.deps import auth, params
from bot_admin_service.api.deps.bot import get_main_bot
from bot_admin_service.db import models
from bot_admin_service.db.dependency import get_session
from bot_admin_service.schemas import RequestParams, PostCreate, PostUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=List[schemas.Post],
)
async def read_posts(
    response: Response,
    current_user: models.User = Depends(auth.get_active_current_user),
    request_params: RequestParams = Depends(
        params.parse_params(models.Post),
    ),
    db: AsyncSession = Depends(get_session),
) -> Any:
    posts, total = await crud.post.get_multi(db, request_params)
    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(posts)}/{total}"
    return posts


@router.get(
    "/{id}",
    response_model=schemas.Post,
)
async def read_post_by_id(
    id: int,
    db: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(auth.get_active_current_user),
) -> Any:
    post = await crud.post.get(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post


@router.put(
    "/{id}",
    response_model=schemas.Post,
)
async def update_post(
    request: Request,
    *,
    id: int,
    post_in: schemas.PostUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(auth.get_active_current_user),
) -> Any:
    post = await crud.post.get(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post_in.files:
        if len(post_in.files) > 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="the number of files must be less than 10",
            )
        if sum(list(map(lambda x: len(bytes(x.file_data)), post_in.files))) > 52428800:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="the size of files must be less than 50MB",
            )
    post = await crud.post.update(db, db_obj=post, obj_in=post_in)
    return post


@router.delete(
    "/{id}",
    response_model=schemas.Post,
)
async def delete_post(
    *,
    id: int,
    db: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(auth.get_active_current_user),
) -> Any:
    post = await crud.post.get(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post = await crud.post.remove(db=db, id=id)
    return post


@router.post("/", response_model=schemas.Post)
async def create_post(
    request: Request,
    post_in: PostCreate,
    current_user: models.User = Depends(auth.get_active_current_user),
    db: AsyncSession = Depends(get_session),
):
    post_in_obj = post_in.copy()
    if post_in.files:
        post_in_obj.files = [x.json() for x in post_in.files]
    post = await crud.post.create(db, obj_in=post_in_obj)
    return post


@router.post("/{id}/publish", response_model=schemas.Post)
async def publish_post(
    request: Request,
    id: int,
    delay: Optional[float] = Param(
        0.1, description="delay in seconds between send messages"
    ),
    current_user: models.User = Depends(auth.get_active_current_user),
    db: AsyncSession = Depends(get_session),
    bot: Bot = Depends(get_main_bot),
):
    post = await crud.post.get(db, id=id)
    text = post.text.replace("<p>", "").replace("</p>", "")
    input_media: list[
        InputMediaPhoto | InputMediaVideo | InputMediaDocument | InputMediaAudio
    ] = []
    if post.files and len(post.files) > 0:
        files = [schemas.ReactFile(**x) for x in post.files]
        for i, pf in enumerate(files):
            media = BufferedInputFile(pf.file_data, pf.filename)
            if pf.content_type.startswith("image"):
                input_media_photo = InputMediaPhoto(
                    media=media,
                    parse_mode=post.parse_mode,
                )
                input_media.append(input_media_photo)
            elif pf.content_type.startswith("video"):
                input_media_video = InputMediaVideo(
                    media=media,
                    parse_mode=post.parse_mode,
                )
                input_media.append(input_media_video)
            elif pf.content_type.startswith("audio"):
                input_media_audio = InputMediaAudio(
                    media=media,
                    parse_mode=post.parse_mode,
                )
                input_media.append(input_media_audio)
            elif pf.content_type.split("/")[0] in ["application", "text"]:
                input_media_document = InputMediaDocument(
                    media=media,
                    parse_mode=post.parse_mode,
                )
                input_media.append(input_media_document)
        if len(input_media) > 0:
            input_media[0].caption = text
    users, total = await crud.bot_user.get_multi(
        db,
        RequestParams(limit=None),
    )
    send_messages_count = 0
    for u in users:
        await asyncio.sleep(delay)
        try:
            if len(input_media) > 0:
                message = await bot.send_media_group(
                    chat_id=u.id,
                    media=input_media,
                )
            else:
                message = await bot.send_message(
                    chat_id=u.id,
                    text=text,
                    parse_mode=post.parse_mode,
                )
            send_messages_count += 1
        except Exception as e:
            logger.error(e)
            return JSONResponse(
                content=str(e.args), status_code=status.HTTP_400_BAD_REQUEST
            )
    post = await crud.post.update(db, db_obj=post, obj_in=PostUpdate(is_published=True))
    return post
