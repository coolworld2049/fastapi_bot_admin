from functools import lru_cache
from typing import Dict
from typing import Type

from bot_admin_service.core.settings.app import AppSettings
from bot_admin_service.core.settings.base import BaseAppSettings
from bot_admin_service.core.settings.base import StageType
from bot_admin_service.core.settings.development import DevAppSettings
from bot_admin_service.core.settings.production import ProdAppSettings
from bot_admin_service.core.settings.test import TestAppSettings

environments: Dict[StageType, Type[AppSettings]] = {
    StageType.dev: DevAppSettings,
    StageType.prod: ProdAppSettings,
    StageType.test: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    stage: StageType = BaseAppSettings().STAGE
    config = environments[stage]
    return config()
