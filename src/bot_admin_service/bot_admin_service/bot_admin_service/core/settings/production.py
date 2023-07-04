import logging
from typing import Optional

from bot_admin_service.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    LOGGING_LEVEL: Optional[int] = logging.INFO
