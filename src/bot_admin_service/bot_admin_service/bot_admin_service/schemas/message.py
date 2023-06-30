

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MessageBase(BaseModel):
    id: Optional[int]
    message: Optional[str]


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class Message(MessageBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
