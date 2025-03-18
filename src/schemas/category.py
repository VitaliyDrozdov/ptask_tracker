from pydantic import BaseModel


class CategoryCreateResponse(BaseModel):
    name: str
    type: str | None = None
