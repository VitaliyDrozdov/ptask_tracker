from dataclasses import dataclass

from src.repository import CategoryRepository
from src.schemas import CategoryCreateResponse


@dataclass
class CategoryService:
    category_repository: CategoryRepository

    async def get_categories(self) -> list[CategoryCreateResponse]:
        return await self.category_repository.get_all_categories()

    async def create_category(
        self, body: CategoryCreateResponse
    ) -> CategoryCreateResponse:
        category = await self.category_repository.create_category(body)
        return CategoryCreateResponse(name=category.name, type=category.type)

    async def get_category(self, category_id: int) -> CategoryCreateResponse:
        return await self.category_repository.get_category(category_id)

    async def delete_category(self, category_id: int) -> bool:
        return await self.category_repository.delete_category(category_id)

    async def update_category(
        self, category_id: int, body: CategoryCreateResponse
    ) -> CategoryCreateResponse:
        category = await self.category_repository.update_category(
            category_id, body
        )
        if not category:
            return None
        return CategoryCreateResponse(name=category.name, type=category.type)
