from loguru import logger
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession

from bot_admin_service.db.session import session


async def get_session() -> AsyncSession:
    s = session()
    try:
        yield s
    except exc.SQLAlchemyError as e:  # noqa
        await s.rollback()
        logger.debug(f"{e.__class__} {e} - ROLLBACK")
    finally:
        await s.close()
