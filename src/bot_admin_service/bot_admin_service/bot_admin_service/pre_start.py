import asyncio
import logging

from loguru import logger
from sqlalchemy import text
from tenacity import after_log
from tenacity import before_log
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed

from bot_admin_service.db.session import engine

max_tries = 60 * 2  # 2 minute
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.INFO),
)
async def init() -> None:
    try:
        async with engine.begin() as conn:
            await conn.execute(text("select 1"))
        logger.info(engine.url)
    except ConnectionRefusedError as ex:
        logger.error(f"{engine.url}, {ex.__class__.__name__} {ex}")


def main() -> None:
    logger.info("Initializing service")
    asyncio.run(init())
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
