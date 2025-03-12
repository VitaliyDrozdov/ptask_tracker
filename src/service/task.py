from dataclasses import dataclass

from src.repository import TaskCacheRepository, TaskRepository
from src.schemas import TaskCreate, TaskResponse


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCacheRepository

    async def get_tasks(self) -> list[TaskResponse]:
        if cache := await self.task_cache.get_tasks():
            return cache
        else:
            tasks = await self.task_repository.get_all_tasks()
            task_schema = [TaskResponse.model_validate(task) for task in tasks]
            await self.task_cache.set_tasks(task_schema)
            return task_schema

    async def create_task(self, body: TaskCreate) -> TaskResponse:
        task_id = await self.task_repository.create_task(body)
        task = await self.task_repository.get_task(task_id)
        return TaskResponse.model_validate(task)

    async def update_task_name(self, task_id: int, name: str) -> TaskResponse:
        task = await self.task_repository.update_task_name(task_id, name)
        # if not task:
        #     raise
        return TaskResponse.model_validate(task)

    async def delete_task(self, task_id: int) -> None:
        task = await self.task_repository.get_task(task_id)
        if not task:
            pass
        await self.task_repository.delete_task(task_id)
