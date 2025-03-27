from dataclasses import dataclass

import pytest

from src.schemas import UserCreateSchema
from tests.fixtures.users.user_model import UserProfileFactory


@dataclass
class FakeUserRepository:
    async def get_user_by_email(self, email: str):
        return None

    async def create_user(self, user_data: UserCreateSchema):
        return UserProfileFactory()


@pytest.fixture
def user_repo():
    return FakeUserRepository()
