from pydantic import BaseModel, Field, model_validator


class TaskCreate(BaseModel):
    id: int
    name: str | None = None
    p_count: int | None = None
    category_id: int = Field(exclude=True, alias="category")

    @model_validator(mode="after")
    def check_name_p_count(self):
        if self.name is None and self.p_count is None:
            raise ValueError("name or p_count must be provided")
        return self
