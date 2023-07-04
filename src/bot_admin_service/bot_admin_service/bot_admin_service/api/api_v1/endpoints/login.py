from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import bot_admin_service.crud as crud
import bot_admin_service.schemas as schemas
from bot_admin_service.api.deps.auth import get_active_current_user
from bot_admin_service.api.exceptions import (
    CouldNotValidateCredentialsException,
)
from bot_admin_service.db.dependency import get_session
from bot_admin_service.services import jwt

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(
    db: AsyncSession = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
) -> Any:
    user = await crud.user.authenticate(
        email=form_data.username,
        password=form_data.password,
        db=db,
    )
    if not user or not await get_active_current_user(user):
        raise CouldNotValidateCredentialsException
    token = jwt.encode_access_token(sub=user.id, user=user)
    return token
