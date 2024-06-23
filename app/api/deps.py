from typing import Generator
from app.db.database import db_helper


async def get_db() -> Generator:
    return db_helper.get_scoped_session()

