import json
import pathlib
import random
import string
from typing import Any

import pytest
from faker import Faker
from loguru import logger
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from bot_admin_service import crud, schemas
from bot_admin_service.core.config import get_app_settings
from bot_admin_service.core.settings.base import StageType
from bot_admin_service.db.utils import create_database
from bot_admin_service.test.utils.random_data import (
    gen_random_password,
    random_lower_string,
)

fake = Faker()


async def create_users(db: AsyncSession, count=100, out_user_creds=None):
    users: list[dict[str, Any]] = [{}]
    test_users: dict[int, dict] = {}
    for i in range(count):
        password = gen_random_password()
        random_phone = "+7" + "".join(
            random.choice(string.digits) for _ in range(10)
        )
        user_in = schemas.UserCreate(
            email=EmailStr(
                f"{i}{random_lower_string(8)}@gmail.com"
            ),
            password=password,
            password_confirm=password,
            username=f"{i}{random.randint(1000, 10000)}",
            full_name=fake.name(),
            age=random.randint(18, 25),
            phone=random_phone,
        )
        user_in_obj = await crud.user.create(db, obj_in=user_in)
        user_in_data = schemas.User(**user_in_obj.__dict__).dict()
        users.append(user_in_data)
        test_users.update({i: user_in_data})
    if out_user_creds and len(users) > 0:
        with open(out_user_creds, "w") as wr:
            wr.write(
                json.dumps(
                    test_users,
                    indent=4,
                    default=str,
                ),
            )
    return users


@pytest.mark.asyncio
async def test_fake_data(db: AsyncSession):
    await create_database(db)
    if get_app_settings().STAGE != StageType.prod:
        count = 20
        out_user_creds = "test_users_creds.json"
        users = await create_users(
            db=db, count=count, out_user_creds=out_user_creds
        )
        logger.info(
            f"users_count - {len(users)}, "
            f"fake user credentials stored in {pathlib.Path().absolute()}/{out_user_creds}"
        )
