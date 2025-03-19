from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies import TaskService, get_task_service
from src.schemas import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["MyTasks"])


@router.get("/all")
async def get_all_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
):
    tasks = await task_service.get_tasks()
    return tasks


@router.post(
    "/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
async def task_create(
    task_service: Annotated[TaskService, Depends(get_task_service)],
    body: TaskCreate,
):
    task = await task_service.create_task(body)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category {body.category_ids} not found.",
        )

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def patch_task(
    task_id: int,
    name: str,
    task_service: Annotated[TaskService, Depends(get_task_service)],
):
    return await task_service.update_task_name(task_id=task_id, name=name)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
):

    deleted = await task_service.delete_task(task_id=task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return {"detail": "Task deleted successfully"}
