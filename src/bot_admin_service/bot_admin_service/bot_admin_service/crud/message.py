from bot_admin_service.crud.base import CRUDBase
from bot_admin_service.db import models
from bot_admin_service.schemas import MessageCreate, MessageUpdate


class CRUDMessage(CRUDBase[models.Message, MessageCreate, MessageUpdate]):
    pass


message = CRUDMessage(models.Message)
