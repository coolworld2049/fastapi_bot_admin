from starlette import status
from starlette.exceptions import HTTPException

from bot_admin_service import schemas
from bot_admin_service.crud.base import CRUDBase
from bot_admin_service.db import models
from bot_admin_service.schemas import PostCreate, PostUpdate


class CRUDPost(CRUDBase[models.Post, PostCreate, PostUpdate]):
    @staticmethod
    def check_files_size(post: models.Post | schemas.Post):
        if post.files:
            files = post.files
            if len(files) > 10:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="the number of files must be less than 10",
                )
            try:
                files_size = sum(list(map(lambda x: len(x.file_data), files)))
            except Exception as fe:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="file data invalid",
                )
            if files_size > 52428800:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="the size of files must be less than 50MB",
                )
            return True
        else:
            return False


post = CRUDPost(models.Post)
