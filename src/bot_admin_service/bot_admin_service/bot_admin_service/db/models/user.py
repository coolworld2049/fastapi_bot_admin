from sqlalchemy import (
    Boolean,
    String,
    BigInteger,
    ForeignKey,
)
from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import TIMESTAMP

from bot_admin_service.db.base import Base, TimestampsMixin


class User(Base, TimestampsMixin):
    id = Column(BigInteger, primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text)
    full_name = Column(String)
    username = Column(String, nullable=False, unique=True)
    telegram_id = Column(BigInteger, ForeignKey("bot_user.id"), nullable=True)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    is_superuser = Column(Boolean, nullable=False, server_default=text("false"))
    is_verified = Column(Boolean, nullable=False, server_default=text("false"))
    verification_token = Column(String(255))
    verified_at = Column(TIMESTAMP(timezone=True), default=None)
