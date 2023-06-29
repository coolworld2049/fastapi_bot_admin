import os
import pathlib
from enum import Enum

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings

load_dotenv()


class StageType(str, Enum):
    dev: str = "dev"
    test: str = "test"
    prod: str = "prod"


class BaseAppSettings(BaseSettings):
    api_prefix: str = "/api/v1"
    docs_url: str = f"{api_prefix}/docs"
    openapi_prefix: str = ""
    openapi_url: str = f"{api_prefix}/openapi.json"
    redoc_url: str = f"{api_prefix}/redoc"

    project_path = pathlib.Path(__file__).parent.parent.parent.parent.parent
    load_dotenv(find_dotenv(f"{project_path}/.env"))
    stage_dotenv = find_dotenv(f'{project_path}/.env.{os.getenv("STAGE", "dev")}')
    load_dotenv(stage_dotenv, override=True) if stage_dotenv else None
    STAGE: StageType = os.getenv("STAGE")
    if STAGE == StageType.dev:
        stage_env_path = pathlib.Path(f"{project_path / '.env'}.{STAGE}")
        load_dotenv(stage_env_path, override=True)
