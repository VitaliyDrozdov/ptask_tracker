from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Categories, Tasks
from src.schemas import TaskCreate, TaskResponse


class TaskRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_task(self, task_id: int):
        query = select(Tasks).where(Tasks.id == task_id)
        task = (await self.db_session.execute(query)).scalars().first()
        return task

    async def get_all_tasks(self, category_ids: Optional[List[int]] = None):
        # if not category_ids:
        #     res = await self.db_session.execute(select(Tasks)).options(
        #         selectinload(Tasks.categories)
        #     )
        # else:
        #     res = await self.db_session.execute(
        #         select(Tasks)
        #         .where(Tasks.categories.any(Categories.id.in_(category_ids)))
        #         .options(selectinload(Tasks.categories))
        #     )
        if not category_ids:
            res = await self.db_session.scalars(
                select(Tasks).options(selectinload(Tasks.categories))
            )
        else:
            res = await self.db_session.scalars(
                select(Tasks)
                .where(Tasks.categories.any(Categories.id.in_(category_ids)))
                .options(selectinload(Tasks.categories))
            )
        tasks = res.all()

        return tasks

    async def create_task(self, task_create: TaskCreate):
        # category_ids = [category.id for category in task_create.category_ids]
        category_ids = task_create.category_ids

        # categories = await self.db_session.execute(
        #     select(Categories).where(Categories.id.in_(category_ids))
        # )
        categories = await self.db_session.scalars(
            select(Categories).where(Categories.id.in_(category_ids))
        )
        categories = categories.all()
        # categories = categories.scalars().all()
        if not categories:
            return None

        new_task = Tasks(
            name=task_create.name,
            p_count=task_create.p_count,
        )
        new_task.categories = categories
        # task = await self.db_session.execute(
        #     insert(Tasks).values(
        #         name=task_create.name,
        #         p_count=task_create.p_count,
        #         categories=categories,
        #     )
        # )
        try:
            self.db_session.add(new_task)
            await self.db_session.flush()
            await self.db_session.commit()
        except SQLAlchemyError:
            await self.db_session.rollback()
            return
        return TaskResponse(
            id=new_task.id,
            name=new_task.name,
            p_count=new_task.p_count,
            category_ids=category_ids,
        )

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
