from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    name: str
    p_count: int
    category_id: int = Field(exclude=True)
