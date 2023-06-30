from loguru import logger
from pydantic import EmailStr
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from bot_admin_service import crud, schemas
from bot_admin_service.core.config import get_app_settings
from bot_admin_service.db.base import Base
from bot_admin_service.db.session import engine, get_db


async def create_first_superuser(db: AsyncSession):
    super_user = await crud.user.get_by_email(
        db,
        email=get_app_settings().FIRST_SUPERUSER_EMAIL,
    )
    if not super_user:
        user_in_admin = schemas.UserCreate(
            email=EmailStr(get_app_settings().FIRST_SUPERUSER_EMAIL),
            password=get_app_settings().FIRST_SUPERUSER_PASSWORD,
            password_confirm=get_app_settings().FIRST_SUPERUSER_PASSWORD,
            full_name="Admin Admin,",
            is_superuser=True,
            is_verified=True,
            username=get_app_settings().FIRST_SUPERUSER_USERNAME,
        )
        super_user = await crud.user.create(db, obj_in=user_in_admin)
        logger.info("created")
    else:
        logger.info("already exists")
    return super_user


async def create_database(db):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await create_first_superuser(db)


async def drop_database() -> None:
    async with engine.connect() as conn:
        disc_users = (
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "
            "FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{get_app_settings().POSTGRESQL_DATABASE}' "
            "AND pid <> pg_backend_pid();"
        )
        await conn.execute(text(disc_users))
        await conn.execute(
            text(f'DROP DATABASE "{get_app_settings().POSTGRESQL_DATABASE}"')
        )
