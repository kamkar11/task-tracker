from fastapi.routing import APIRouter

from .tasks_router import api_tasks_router

main_router = APIRouter(prefix="/v1")

main_router.include_router(api_tasks_router)