from fastapi import status, HTTPException
from fastapi.routing import APIRouter

from common.dependencies.session import SessionDep
from common.schemas.tasks import Task, TaskCreate, TaskUpdate
from common.repositories.task_repository import TaskRepository


api_tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@api_tasks_router.post("/tasks", status_code=status.HTTP_200_OK, response_model=Task)
async def create_task(task: TaskCreate, db: SessionDep):
    return TaskRepository(db).create(task)

@api_tasks_router.get("/tasks", status_code=status.HTTP_200_OK, response_model=list[Task])
async def read_tasks(db: SessionDep):
    return TaskRepository(db).get_all()

@api_tasks_router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=Task)
async def read_task(task_id: int, db: SessionDep):
    task = TaskRepository(db).get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@api_tasks_router.put("/tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=Task)
async def update_task(task_id: int, task: TaskUpdate, db: SessionDep):
    updated = TaskRepository(db).update(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@api_tasks_router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=Task)
async def delete_task(task_id: int, db: SessionDep):
    deleted = TaskRepository(db).delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted