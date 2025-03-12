from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.cache import get_cache_session
from dependencies.db import get_db_session  # noqa
from src.repository import TaskCacheRepository, TaskRepository
from src.service import TaskService


async def get_task_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return TaskRepository(db_session)


async def get_task_cache_repository() -> TaskCacheRepository:
    conn = get_cache_session()
    return TaskCacheRepository(conn)


async def get_task_service(
    task_repository: Annotated[TaskRepository, Depends(get_task_repository)],
    task_cache: Annotated[
        TaskCacheRepository, Depends(get_task_cache_repository)
    ],
) -> TaskService:
    return TaskService(task_repository, task_cache)
