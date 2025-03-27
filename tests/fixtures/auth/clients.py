from dataclasses import dataclass

import httpx
import pytest
from faker import Faker

from src.schemas import GoogleUserData
from src.settings import Settings

faker = Faker()


@dataclass
class FakeGoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> GoogleUserData:
        # access_token = await self._get_user_access_token(code=code)
        return google_user_info_data()

    async def _get_user_access_token(self, code: str) -> str:
        return f"fake_access_token {code}"


@pytest.fixture
def google_client():
    return FakeGoogleClient(
        settings=Settings, async_client=httpx.AsyncClient()
    )


@dataclass
class FakeYandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> dict:
        access_token = await self._get_user_access_token(code=code)
        return {"fake_access_token": access_token}

    async def _get_user_access_token(self, code: str) -> str:
        return f"fake_access_token {code}"


@pytest.fixture
def yandex_client():
    return FakeYandexClient(
        settings=Settings, async_client=httpx.AsyncClient()
    )


def google_user_info_data() -> GoogleUserData:
    return GoogleUserData(
        id=faker.random_int(),
        email=faker.email(),
        name=faker.name(),
        verified_email=True,
        access_token=faker.sha256(),
    )
