from sqlalchemy import Column, BigInteger, String, Boolean, JSON

from bot_admin_service.db import Base
from bot_admin_service.db.base import TimestampsMixin


class Post(Base, TimestampsMixin):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(String, unique=True)
    files = Column(JSON)
    parse_mode = Column(String)
    is_published = Column(Boolean)
