import factory.fuzzy
from faker import Faker
from pytest_factoryboy import register

from src.schemas import UserLoginSchema

faker = Faker()

EXISTING_GOOGLE_ID = 20
EXISTING_GOOGLE_USER_EMAIL = "test@gmail.com"


@register(_name="user_profile")
class UserProfileFactory(factory.Factory):
    class Meta:
        model = UserLoginSchema

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.name())
    email = factory.LazyFunction(lambda: faker.email())
    name = factory.LazyFunction(lambda: faker.name())
