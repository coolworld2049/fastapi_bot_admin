from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import bot_admin_service.crud as crud
import bot_admin_service.schemas as schemas
from bot_admin_service.api.deps import auth
from bot_admin_service.api.deps import params
from bot_admin_service.api.exceptions import DuplicateUserException
from bot_admin_service.core.config import get_app_settings
from bot_admin_service.db import models
from bot_admin_service.db.dependency import get_session
from bot_admin_service.db.models import User
from bot_admin_service.schemas import RequestParams

router = APIRouter()


@router.get(
    "/",
    response_model=List[schemas.User],
)
async def read_users(
    response: Response,
    current_user: models.User = Depends(auth.get_active_current_user),
    request_params: RequestParams = Depends(
        params.parse_params(User),
    ),
    db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Retrieve users.
    """
    users, total = await crud.user.get_multi(db, request_params)
    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(users)}/{total}"
    return users


@router.post(
    "/",
    response_model=schemas.User,
)
async def create_user(
    *,
    db: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(auth.get_active_current_user),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise DuplicateUserException
    user = await crud.user.create(db, obj_in=user_in)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return user


@router.put(
    "/me",
    response_model=schemas.User,
)
async def update_user_me(
    user_in: schemas.UserUpdateMe,
    db: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(auth.get_active_current_user),
) -> Any:
    """
    Update own user.
    """
    user = await crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get(
    "/me",
    response_model=schemas.User,
)
async def read_user_me(
    db: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(auth.get_active_current_user),
) -> Any:
    """
    Get current user.
    """
    user = await crud.user.get(db, current_user.id)
    return user


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
    Get a specific user.
    """
    user = await crud.user.get(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.put(
    "/{id}",
    response_model=schemas.User,
)
async def update_user(
    *,
    id: int,
    db: AsyncSession = Depends(get_session),
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(auth.get_active_current_user),
) -> Any:
    """
    Update a user.
    """
    user = await crud.user.get(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user = await crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete(
    "/{id}",
    response_model=schemas.User,
)
async def delete_user(
    *,
    id: int,
    db: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(auth.get_active_current_user),
) -> Any:
    """
    Delete user
    """
    user = await crud.user.get(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if id == current_user.id or user.email == get_app_settings().FIRST_SUPERUSER_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Forbidden to delete",
        )
    user = await crud.user.remove(db=db, id=id)
    return user
