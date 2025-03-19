from typing import Annotated

# isort: skip file
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.cache import get_cache_session
from src.dependencies.db import get_db_session  # noqa
from src.repository import TaskCacheRepository  # noqa
from src.repository import CategoryRepository, TaskRepository  # noqa
from src.service import CategoryService, TaskService


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


async def get_category_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return CategoryRepository(db_session)


async def get_category_service(
    category_repository: Annotated[
        CategoryRepository, Depends(get_category_repository)
    ],
):
    return CategoryService(category_repository)
