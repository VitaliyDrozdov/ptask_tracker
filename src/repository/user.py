from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserProfile
from src.schemas import UserCreateSchema


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def get_user_by_email(self, email: str):
        query = select(UserProfile).where(UserProfile.email == email)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def create_user(self, user_create: UserCreateSchema):
        query = (
            insert(UserProfile)
            .values(**user_create.model_dump(exclude_none=True))
            .returning(UserProfile.id)
        )
        async with self.db_session as session:
            user_id: int = await session.execute(query).scalar()
            await session.flush()
            await session.commit()
            return await self.get_user(user_id)

    async def get_user(self, user_id: int):
        query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def get_user_by_username(self, username: str):
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()
