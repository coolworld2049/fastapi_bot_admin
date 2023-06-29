import logging

from bot_admin_service.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    LOGGING_LEVEL: int = logging.DEBUG
