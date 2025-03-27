import datetime as dt

import pytest
from jose import jwt

from src.schemas import UserLoginSchema
from src.service import AuthService
from src.settings import Settings

pytestmark = pytest.mark.asyncio


async def test_get_googgle_redirect_url_success(
    auth_service: AuthService, settings: Settings
):
    assert isinstance(auth_service, AuthService)
    settings_google_redirect_url = settings.google_redirect_url
    auth_service_google_redirect_url = auth_service.get_google_redirect_url()
    assert isinstance(auth_service_google_redirect_url, str)
    assert settings_google_redirect_url == auth_service_google_redirect_url


async def test_generate_access_token_success(
    auth_service: AuthService, settings: Settings
):
    user_id = "1"
    access_token = auth_service.generate_access_token(user_id=user_id)
    decoded_access_token = jwt.decode(
        access_token, key=settings.secret_key, algorithms="HS256"
    )
    # decoded_user_id = decoded_access_token.get("user_id")
    decoded_token_expire = dt.datetime.fromtimestamp(
        decoded_access_token.get("expire"), tz=dt.timezone.utc
    )

    assert (decoded_token_expire - dt.datetime.now(tz=dt.UTC)) > dt.timedelta(
        days=6
    )


async def test_get_user_id_from_access_token_success(
    auth_service: AuthService,
):
    user_id = str(1)
    access_token = auth_service.generate_access_token(user_id=user_id)
    decoded_user_id = auth_service.get_user_id_from_token(access_token)
    assert decoded_user_id == user_id


async def test_google_auth_success(auth_service: AuthService):
    code = "fake_code"
    user = await auth_service.google_auth(code=code)
    decoded_user_id = auth_service.get_user_id_from_token(user.access_token)
    assert user.user_id == decoded_user_id
    assert isinstance(user, UserLoginSchema)
