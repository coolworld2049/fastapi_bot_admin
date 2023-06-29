from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BotUserBase(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]


class BotUserCreate(BotUserBase):
    pass


class BotUserUpdate(BotUserBase):
    pass


class BotUser(BotUserBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
