from dataclasses import dataclass

from src.repository import CategoryRepository
from src.schemas import CategoryCreate, CategoryResponse


@dataclass
class CategoryService:
    category_repository: CategoryRepository

    async def get_categories(self) -> list[CategoryResponse]:
        return await self.category_repository.get_all_categories()

    async def create_category(self, body: CategoryCreate) -> CategoryCreate:
        category = await self.category_repository.create_category(body)
        return CategoryResponse(
            name=category.name, type=category.type, id=category.id
        )

    async def get_category(self, category_id: int) -> CategoryResponse:
        return await self.category_repository.get_category(category_id)

    async def delete_category(self, category_id: int) -> bool:
        return await self.category_repository.delete_category(category_id)

    async def update_category(
        self, category_id: int, body: CategoryCreate
    ) -> CategoryResponse:
        category = await self.category_repository.update_category(
            category_id, body
        )
        if not category:
            return None
        return CategoryResponse(
            name=category.name, type=category.type, id=category.id
        )
