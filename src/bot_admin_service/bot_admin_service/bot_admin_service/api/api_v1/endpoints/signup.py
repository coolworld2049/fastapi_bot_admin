from fastapi import APIRouter
from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from bot_admin_service import crud, schemas
from bot_admin_service.db.dependency import get_session
from bot_admin_service.api.exceptions import DuplicateUserException
from bot_admin_service.core.config import get_app_settings
from bot_admin_service.services.email import Email

router = APIRouter()


@router.post(
    "/client",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
async def signup_client(
    user_in: schemas.UserCreateOpen,
    db: AsyncSession = Depends(get_session),
):
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise DuplicateUserException
    obj_in = schemas.UserCreate(
        **user_in.dict(exclude_unset=True)
    )
    user = await crud.user.create(db, obj_in=obj_in)
    if get_app_settings().USE_EMAILS:
        email = Email(EmailStr(get_app_settings().SMTP_FROM))
        res = await crud.user.send_email_for_verif(
            db,
            db_obj=user,
            email=email,
        )
        if not res:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="There was an error sending email",
            )
    return {"msg": "The confirmation code has been sent to your email"}
