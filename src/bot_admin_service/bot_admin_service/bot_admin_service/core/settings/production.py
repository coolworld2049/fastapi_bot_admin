import logging

from bot_admin_service.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    LOGGING_LEVEL = logging.INFO
