from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    type: str | None = None


class CategoryResponse(BaseModel):
    name: str
    type: str | None = None
    id: int


class CategorySub(BaseModel):
    id: int
