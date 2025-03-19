from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies import CategoryService, get_category_service
from src.schemas import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryResponse])
async def get_all_categories(
    category_service: Annotated[
        CategoryService, Depends(get_category_service)
    ],
):
    return await category_service.get_categories()


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category_service: Annotated[
        CategoryService, Depends(get_category_service)
    ],
    body: CategoryCreate,
):
    return await category_service.create_category(body)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_cateogory(
    category_service: Annotated[
        CategoryService, Depends(get_category_service)
    ],
    body: CategoryCreate,
    category_id: int,
):
    category = await category_service.update_category(category_id, body)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found",
        )
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    category_service: Annotated[
        CategoryService, Depends(get_category_service)
    ],
):
    deleted = await category_service.delete_category(category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found",
        )
    return {"detail": "Category deleted successfully"}
