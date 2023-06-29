import asyncio
import logging

from bot_admin_service.db.session import get_db
from bot_admin_service.db.utils import create_database


async def main() -> None:
    logging.info("Creating initial data")
    async with get_db() as db:
        await create_database(db)
    logging.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
