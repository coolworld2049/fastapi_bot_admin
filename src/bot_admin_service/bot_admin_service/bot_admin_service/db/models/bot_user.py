from sqlalchemy import Column, BigInteger, String

from bot_admin_service.db import Base
from bot_admin_service.db.base import TimestampsMixin


class BotUser(Base, TimestampsMixin):
    id = Column(BigInteger, primary_key=True, autoincrement=False)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    language_code = Column(String)
