import datetime
from dataclasses import dataclass
from datetime import datetime as dt
from datetime import timedelta

from jose import JWTError, jwt

from src.models import UserProfile
from src.repository import UserRepository
from src.schemas import UserLoginSchema
from src.settings import settings

from src.exceptions.exceptions import (  # isort: skip
    IncorrectPassword,  # isort: skip
    TaskNotCorrect,  # isort: skip
    UserNotFoundException,  # isort: skip
)


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: settings

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
            claims=payload, key=settings.secret_key, algorithm="HS256"
        )

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    def get_user_id_from_token(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token=token, key=settings.secret_key, algorithms="HS256"
            )
        except JWTError:
            raise TaskNotCorrect
        return payload["user_id"]
