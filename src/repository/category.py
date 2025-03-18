from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Categories
from src.schemas import CategoryCreateResponse


class CategoryRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_category(self, category_id: int):
        query = select(Categories).where(Categories.id == category_id)
        return await self.db_session.execute(query).scalar()

    async def get_all_categories(self):
        return (
            await self.db_session.execute(select(Categories)).scalars().all()
        )

    async def create_category(self, category_create: CategoryCreateResponse):
        category = Categories(
            name=category_create.name, type=category_create.type
        )
        self.db_session.add(category)
        await self.db_session.flush()
        await self.db_session.commit()
        return category.id

    async def delete_category(self, category_id: int):
        res = await self.db_session.execute(
            delete(Categories).where(Categories.id == category_id)
        )
        if res.rowcount == 0:
            return False
        await self.db_session.commit()
        return True

    async def update_category(
        self, category_id: int, category_update: CategoryCreateResponse
    ):
        category = await self.db_session.execute(
            update(Categories)
            .where(Categories.id == category_id)
            .value(name=category_update.name, type=category_update.type)
            .returning(Categories)
        ).scalar()
        if not category:
            return None
        await self.db_session.commit()
        return category.name, category.type
