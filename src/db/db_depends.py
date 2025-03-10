from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.settings import DBConfig


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with DBConfig.async_sessionmaker_() as session:
        yield session
