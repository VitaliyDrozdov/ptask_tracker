from sqlalchemy.orm import Mapped, mapped_column

from src.settings import Base


class UserProfile(Base):
    __tablename__ = "UserProfile"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=True)
    passoword: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str | None]
    name: Mapped[str | None]
