from fastapi import status
from fastapi.routing import APIRouter

api_tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@api_tasks_router.get("", status_code=status.HTTP_200_OK, response_model=TasksResponse)
async def get_tasks():
    return "tasks"