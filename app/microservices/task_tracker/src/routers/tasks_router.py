from fastapi import status
from fastapi.routing import APIRouter

from common.schemas.tasks import TaskResponse

api_tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@api_tasks_router.get("", status_code=status.HTTP_200_OK)
async def get_tasks():
    return "tasks"