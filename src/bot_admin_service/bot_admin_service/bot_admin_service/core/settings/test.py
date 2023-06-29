import logging

from bot_admin_service.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    LOGGING_LEVEL: int = logging.DEBUG

    USE_RBAC = False
    USE_USER_CHECKS = False
    USE_EMAILS = False
