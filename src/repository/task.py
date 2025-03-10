from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Tasks


class TaskRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_task(self, task_id: int):
        query = select(Tasks).where(Tasks.id == task_id)
        async with self.db_session as session:
            task = (await session.execute(query)).scalars().first()
        return task

    async def get_all_tasks(self, category_ids: Optional[List[int]] = None):
        async with self.db_session as session:
            if not category_ids:
                res = await session.execute(select(Tasks))
            else:
                res = await session.execute(
                    select(Tasks).where(Tasks.category_id.in_(category_ids))
                )
            tasks = res.scalars().all()
        return tasks

    async def create_task(self, task: Tasks):
        async with self.db_session as session:
            session.add(task)
            await session.flush()
            await session.commit()

    async def delete_task(self, task_id: int):
        async with self.db_session as session:
            await session.execute(delete(Tasks).where(Tasks.id == task_id))
            await session.commit()
