from bot_admin_service.crud.base import CRUDBase
from bot_admin_service.db import models
from bot_admin_service.schemas.bot_user import BotUserUpdate, BotUserCreate


class CRUDBotUser(CRUDBase[models.BotUser, BotUserCreate, BotUserUpdate]):
    pass


bot_user = CRUDBotUser(models.BotUser)
