from typing import Annotated

from fastapi import APIRouter, Depends

from src.dependencies import get_user_service
from src.schemas import UserCreateSchema, UserLoginSchema
from src.service import UserService

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/", response_model=UserLoginSchema)
async def create_user(
    body: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(
        username=body.username, password=body.password
    )
