import pytest

from src.settings import Settings


@pytest.fixture
def settings():
    return Settings()
