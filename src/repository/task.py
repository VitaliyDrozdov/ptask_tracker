from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Categories, Tasks
from src.schemas import TaskCreate


class TaskRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_task(self, task_id: int):
        query = select(Tasks).where(Tasks.id == task_id)
        task = (await self.db_session.execute(query)).scalars().first()
        return task

    async def get_all_tasks(self, category_ids: Optional[List[int]] = None):
        if not category_ids:
            res = await self.db_session.execute(select(Tasks))
        else:
            res = await self.db_session.execute(
                select(Tasks).where(Tasks.categories.in_(category_ids))
            )
        tasks = res.scalars().all()
        return tasks

    async def create_task(self, task_create: TaskCreate):
        category_ids = (
            task_create.category_ids
            if isinstance(task_create.category_ids, list)
            else [task_create.category_ids]
        )
        categories = await self.db_session.execute(
            select(Categories).where(Categories.id.in_(category_ids))
        )
        categories = categories.scalars().all()
        if not categories:
            return
        task = Tasks(
            name=task_create.name,
            p_count=task_create.p_count,
            categories=categories,
        )
        self.db_session.add(task)
        await self.db_session.flush()
        await self.db_session.commit()
        return task

    async def delete_task(self, task_id: int):
        async with self.db_session as session:
            res = await session.execute(
                delete(Tasks).where(Tasks.id == task_id)
            )
            if res.rowcount == 0:
                return False
            await session.commit()
            return True

    async def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = (
            update(Tasks)
            .where(Tasks.id == task_id)
            .values(name=name)
            .returning(Tasks.id)
        )
        task_id: int = await self.db_session.execute(
            query
        ).scalar_one_or_none()
        await self.db_session.commit()
        await self.db_session.flush()
        return await self.get_task(task_id)
