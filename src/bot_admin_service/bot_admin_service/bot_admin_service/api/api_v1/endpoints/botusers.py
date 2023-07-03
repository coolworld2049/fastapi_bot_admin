from typing import List, Any

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from bot_admin_service import schemas, crud
from bot_admin_service.api.deps import auth, params
from bot_admin_service.db import models, BotUser
from bot_admin_service.db.dependency import get_session
from bot_admin_service.schemas import RequestParams

router = APIRouter()


@router.get(
    "/",
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
    "/{id}",
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
