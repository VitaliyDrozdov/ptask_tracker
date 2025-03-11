from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.repository import TaskRepository, get_tasks_repository
from src.schemas import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["MyTasks"])


@router.get("/all", response_model=list[TaskResponse])
async def get_all_tasks(
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
):
    return await task_repository.get_all_tasks()


@router.post(
    "/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
async def task_create(
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
    create_task: TaskCreate,
):
    task = await task_repository.create_task(create_task)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category {create_task.category_ids} not found.",
        )

    return {"transaction": "succesfull", "task_id": task.id}
