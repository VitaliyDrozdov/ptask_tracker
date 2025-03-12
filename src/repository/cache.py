import json

from redis import asyncio as redis

from src.schemas import TaskCreate


class TaskCache:
    def __init__(self, redis: redis):
        self.redis = redis

    async def get_tasks(self) -> list[TaskCreate]:
        async with self.redis as r:
            task_json = await r.lrange("tasks", 0, -1)
            return [
                TaskCreate.model_validate(json.loads(task))
                for task in task_json
            ]

    async def set_tasks(self, tasks: list[TaskCreate]):
        tasks_json = [task.model_dump_json() for task in tasks]
        async with self.redis as r:
            await r.lpush("tasks", *tasks_json)
