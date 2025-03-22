import datetime
from dataclasses import dataclass
from datetime import datetime as dt
from datetime import timedelta

from jose import JWTError, jwt

from src.models import UserProfile
from src.repository import UserRepository
from src.schemas import UserCreateSchema, UserLoginSchema
from src.service.client import GoogleClient, YandexClient
from src.settings.settings_all import settings as settings_

from src.exceptions.exceptions import (  # isort: skip
    IncorrectPassword,  # isort: skip
    TaskNotCorrect,  # isort: skip
    UserNotFoundException,  # isort: skip
)


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: settings_
    google_client: GoogleClient
    yandex_client: YandexClient

    async def google_auth(self, code: str):
        user_data = await self.google_client.get_user_info(code)
        if user := await self.user_repository.get_user_by_email(
            email=user_data.email
        ):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        create_user_data = UserCreateSchema(
            email=user_data.email, name=user_data.name
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(
            user_id=created_user.id, access_token=access_token
        )

    async def yandex_auth(self, code: str):
        user_data = await self.yandex_client.get_user_info(code=code)

        if user := await self.user_repository.get_user_by_email(
            email=user_data.default_email
        ):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            yandex_access_token=user_data.access_token,
            email=user_data.default_email,
            name=user_data.name,
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(
            user_id=created_user.id, access_token=access_token
        )

    def get_google_redirect_url(self):
        return self.settings.google_redirect_url

    def get_yandex_redirect_url(self):
        return self.settings.yandex_redirect_url

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.passoword != password:
            raise IncorrectPassword

    def generate_access_token(self, user_id: int):
        payload = {
            "user_id": user_id,
            "expire": (
                dt.now(tz=datetime.UTC) + timedelta(days=7)
            ).timestamp(),
        }
        return jwt.encode(
            claims=payload, key=self.settings.secret_key, algorithm="HS256"
        )

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    def get_user_id_from_token(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token=token, key=self.settings.secret_key, algorithms="HS256"
            )
        except JWTError:
            raise TaskNotCorrect
        return payload["user_id"]
