from typing import Optional

from pydantic import BaseModel

from bot_admin_service.db import models


class Token(BaseModel):
    access_token: str
    token_type: Optional[str] = "bearer"


class TokenPayload(BaseModel):
    sub: str
    user: models.User | str
    exp: int

    class Config:
        arbitrary_types_allowed = True
