from typing import AsyncGenerator

from redis import asyncio as redis

from src.settings import settings

# def get_redis_connection() -> redis.Redis:
#     return redis.Redis(
#         host=settings.CACHE_HOST,
#         port=settings.CACHE_PORT,
#         db=settings.CACHE_DB,
#     )


async def get_cache_session() -> AsyncGenerator[redis.Redis, None]:
    cache_session = redis.Redis(
        host=settings.CACHE_HOST,
        port=settings.CACHE_PORT,
        db=settings.CACHE_DB,
        decode_responses=True,
    )
    try:
        yield cache_session
    finally:
        await cache_session.aclose()
