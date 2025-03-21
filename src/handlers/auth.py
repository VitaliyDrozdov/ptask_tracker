from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_auth_service
from src.exceptions.exceptions import IncorrectPassword, UserNotFoundException
from src.schemas import UserCreateSchema, UserLoginSchema
from src.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=UserLoginSchema)
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        return await auth_service.login(body.username, body.password)

    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)

    except IncorrectPassword as e:
        raise HTTPException(status_code=401, detail=e.detail)
