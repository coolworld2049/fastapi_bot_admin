from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

import bot_admin_service.crud as crud
from bot_admin_service.api.exceptions import (
    CouldNotValidateCredentialsException,
    AccountNotVerifiedException,
)
from bot_admin_service.core.config import get_app_settings
from bot_admin_service.db import models
from bot_admin_service.db.dependency import get_session
from bot_admin_service.services.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{get_app_settings().api_prefix}/login/access-token"
)


async def get_current_user(
    db: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> models.User:
    token_data = decode_access_token(token)
    user = await crud.user.get(db=db, id=int(token_data.sub))
    if not user:
        raise CouldNotValidateCredentialsException
    return user


async def get_verified_current_user(
    user=Depends(get_current_user),
):
    if get_app_settings().USE_EMAILS:
        if not user.is_verified:
            raise AccountNotVerifiedException
    return user


async def get_active_current_user(
    user=Depends(get_verified_current_user),
):
    if not user.is_active:
        raise AccountNotVerifiedException
    return user
