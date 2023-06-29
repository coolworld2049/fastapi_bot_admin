import time
from contextlib import asynccontextmanager

from loguru import logger
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from bot_admin_service.core.config import get_app_settings

engine = create_async_engine(get_app_settings().postgres_asyncpg_url)
session = async_sessionmaker(engine, autocommit=False)

if get_app_settings().SQLALCHEMY_PROFILE_QUERY_MODE:

    def before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        conn.info.setdefault("query_start_time", []).append(time.time())
        logger.debug(f"Start Query: {statement}")

    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = time.time() - conn.info["query_start_time"].pop(-1)
        logger.debug("Query Complete!")
        logger.debug("Total Time: %f" % total)

    event.listen(
        engine.sync_engine,
        "before_cursor_execute",
        before_cursor_execute,
    )
    event.listen(
        engine.sync_engine,
        "after_cursor_execute",
        after_cursor_execute,
    )


@asynccontextmanager
async def get_db() -> AsyncSession:
    s = session()
    try:
        await s.begin()
        yield s
        await s.commit()
    except Exception as e:  # noqa
        logger.debug(f"{e.__class__} {e} - ROLLBACK")
        await s.rollback()
    finally:
        await s.close()
