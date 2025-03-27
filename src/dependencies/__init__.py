from typing import Annotated

# isort: skip file
import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.cache import get_cache_session
from src.dependencies.db import get_db_session  # noqa
from src.repository import TaskCacheRepository  # noqa
from src.repository import CategoryRepository, TaskRepository, UserRepository
from src.service import AuthService, CategoryService, TaskService, UserService
from src.service.auth import GoogleClient, YandexClient
from src.settings import settings


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


async def get_user_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_google_client(
    async_client: httpx.AsyncClient = Depends(get_async_client),
) -> GoogleClient:
    return GoogleClient(settings=settings, async_client=async_client)


async def get_yandex_client(
    async_client: httpx.AsyncClient = Depends(get_async_client),
) -> YandexClient:
    return YandexClient(settings=settings, async_client=async_client)


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client),
    yandex_client: YandexClient = Depends(get_yandex_client),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=settings,
        google_client=google_client,
        yandex_client=yandex_client,
    )


async def get_user_service(
    user_repository: UserRepository = Depends(get_task_repository),
    auth_service=Depends(get_auth_service),
) -> UserService:
    return UserService(
        user_repository=user_repository, auth_service=auth_service
    )
