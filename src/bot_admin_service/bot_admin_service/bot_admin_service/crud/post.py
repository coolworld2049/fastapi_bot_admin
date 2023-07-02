from bot_admin_service.crud.base import CRUDBase
from bot_admin_service.db import models
from bot_admin_service.schemas import PostCreate, PostUpdate


class CRUDPost(CRUDBase[models.Post, PostCreate, PostUpdate]):
    pass


post = CRUDPost(models.Post)
