import pytest

from src.dependencies import AuthService
from src.settings import Settings


@pytest.fixture
def auth_service(google_client, yandex_client, user_repo):
    return AuthService(
        user_repository=user_repo,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
    )
