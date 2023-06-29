import logging

from bot_admin_service.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    LOGGING_LEVEL: int = logging.DEBUG

    USE_EMAILS = False
