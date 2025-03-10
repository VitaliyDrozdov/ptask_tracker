from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.settings import Base

tasks_categories = Table(
    "tasks_categories",
    Base.metadata,
    Column("tasks_id", ForeignKey("tasks.id"), primary_key=True),
    Column("categories_id", ForeignKey("categories.id"), primary_key=True),
)


class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    p_count: Mapped[int] = mapped_column(Integer)
    # category_id: Mapped[int] = mapped_column(
    #     Integer, ForeignKey("categories.id"), nullable=False
    # )
    categories: Mapped["Categories"] = relationship(
        "Categories", back_populates="tasks", secondary=tasks_categories
    )


class Categories(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(50), nullable=True)
    tasks: Mapped[list["Tasks"]] = relationship(
        "Tasks",
        back_populates="categories",
        uselist=True,
        single_parent=False,
        secondary=tasks_categories,
    )
