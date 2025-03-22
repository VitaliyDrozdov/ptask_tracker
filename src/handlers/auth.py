from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

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


@router.get("/login/google", response_class=RedirectResponse)
async def google_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    redirect_url = auth_service.get_google_redirect_url()
    return RedirectResponse(redirect_url)


@router.get("/google")
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str
):
    return await auth_service.google_auth(code)


@router.get("/login/yandex", response_class=RedirectResponse)
async def yandex_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    redirect_url = auth_service.get_yandex_redirect_url()
    return RedirectResponse(redirect_url)


@router.get("/yandex")
async def yandex_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str
):
    return await auth_service.yandex_auth(code)
