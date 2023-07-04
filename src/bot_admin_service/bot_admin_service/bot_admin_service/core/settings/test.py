import logging
from typing import Optional

from bot_admin_service.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    LOGGING_LEVEL: Optional[int] = logging.DEBUG

    USE_EMAILS = False
