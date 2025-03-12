import json
from typing import Any

from redis import asyncio as redis

from src.schemas import TaskResponse


class TaskCacheRepository:
    def __init__(self, redis: redis):
        self.cache = redis

    async def get_all_tasks(self, key: str = "all_tasks") -> list[Any] | None:
        tasks_json = await self.cache.get(key)
        if not tasks_json:
            return
        return [
            TaskResponse.model_validate(task)
            for task in json.loads(tasks_json)
        ]

    async def set_all_tasks(
        self, tasks: list[TaskResponse], key: str = "all_tasks"
    ) -> None:
        tasks_json = json.dumps(
            [task.model_dump() for task in tasks], ensure_ascii=False
        )
        await self.cache.set(key, tasks_json, ex=60)

    # старая версия:
    # async def get_all_tasks(self) -> list[TaskResponse]:
    #     async with self.redis as r:
    #         task_json = await r.lrange("tasks", 0, -1)
    #         return [
    #             TaskResponse.model_validate(json.loads(task))
    #             for task in task_json
    #         ]

    # async def set_tasks(self, tasks: list[TaskResponse]):
    #     tasks_json = [task.model_dump_json() for task in tasks]
    #     async with self.redis as r:
    #         await r.lpush("tasks", *tasks_json)
