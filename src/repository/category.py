from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Categories
from src.schemas import CategoryCreate


class CategoryRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_category(self, category_id: int):
        query = select(Categories).where(Categories.id == category_id)
        return await self.db_session.execute(query).scalar()

    async def get_all_categories(self):
        categories = await self.db_session.execute(select(Categories))
        categories = categories.scalars().all()
        return categories

    async def create_category(self, category_create: CategoryCreate):
        category = Categories(
            name=category_create.name, type=category_create.type
        )
        self.db_session.add(category)
        await self.db_session.flush()
        await self.db_session.commit()
        return category

    async def delete_category(self, category_id: int):
        res = await self.db_session.execute(
            delete(Categories).where(Categories.id == category_id)
        )
        if res.rowcount == 0:
            return False
        await self.db_session.commit()
        return True

    async def update_category(
        self, category_id: int, category_update: CategoryCreate
    ):
        category = await self.db_session.execute(
            update(Categories)
            .where(Categories.id == category_id)
            .values(name=category_update.name, type=category_update.type)
            .returning(Categories)
        )
        category = category.scalar_one_or_none()
        if not category:
            return None
        await self.db_session.commit()
        return category
