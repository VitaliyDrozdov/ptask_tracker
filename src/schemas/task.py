from pydantic import BaseModel, model_validator


class TaskCreate(BaseModel):
    name: str | None = None
    p_count: int | None = None
    category_ids: list[int]

    @model_validator(mode="after")
    def check_name_p_count(self):
        if self.name is None and self.p_count is None:
            raise ValueError("name or p_count must be provided")
        return self


class TaskResponse(BaseModel):
    id: int
    name: str | None = None
    p_count: int | None = None
    category_ids: list[int]
