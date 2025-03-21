from dataclasses import dataclass

from src.repository import UserRepository
from src.schemas import UserCreateSchema, UserLoginSchema
from src.service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(
        self, username: str, password: str
    ) -> UserLoginSchema:
        user_create_data = UserCreateSchema(
            username=username, password=password
        )
        user = await self.user_repository.create_user(
            user_create=user_create_data
        )
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
