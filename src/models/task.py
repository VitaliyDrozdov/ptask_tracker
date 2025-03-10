from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    p_count: Mapped[int]
    category_id: Mapped[int]


class Categories(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str] = mapped_column(nullable=True)
