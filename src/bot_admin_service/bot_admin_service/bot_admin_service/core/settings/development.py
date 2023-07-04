import logging
from typing import Optional

from bot_admin_service.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    LOGGING_LEVEL: Optional[int] = logging.DEBUG
