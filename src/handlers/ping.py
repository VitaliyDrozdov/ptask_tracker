from fastapi import APIRouter

from schemas.task import Task

router = APIRouter(prefix="/ping", tags=["Ping"])


@router.get("/", response_model=Task)
async def ping(name: str, task: Task):
    return {"message": "ok"}
