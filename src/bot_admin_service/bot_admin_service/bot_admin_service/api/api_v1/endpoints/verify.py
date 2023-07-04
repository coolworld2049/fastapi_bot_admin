from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

import bot_admin_service.crud as crud
from bot_admin_service.api.exceptions import (
    InvalidVerificationTokenException,
)
from bot_admin_service.db import models
from bot_admin_service.db.dependency import get_session

router = APIRouter()


@router.get("/email/{token}")
async def verify_me(
    token: str,
    db: AsyncSession = Depends(get_session),
):
    user = await crud.user.get_by_attr(
        db, where_clause=models.User.verification_token == token
    )
    if not user or user.is_verified:
        raise InvalidVerificationTokenException
    await crud.user.verify_token_from_email(db, db_obj=user, token=token)
    return {"msg": "Verified"}
