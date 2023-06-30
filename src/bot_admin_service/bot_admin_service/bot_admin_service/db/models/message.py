from sqlalchemy import Column, BigInteger, JSON

from bot_admin_service.db import Base
from bot_admin_service.db.base import TimestampsMixin


class Message(Base, TimestampsMixin):
    id = Column(BigInteger, primary_key=True)
    message = Column(JSON)
