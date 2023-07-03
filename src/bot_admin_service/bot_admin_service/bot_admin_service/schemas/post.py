from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from bot_admin_service.schemas.react_file import ReactFile


class PostBase(BaseModel):
    text: Optional[str]
    files: Optional[list[ReactFile] | list[str]] = None
    parse_mode: Optional[str] = "HTML"
    is_published: Optional[bool] = False


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class PostDetails(Post):
    users_count: Optional[int]
    sent_count: Optional[int]
