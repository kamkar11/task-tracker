import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from datetime import datetime, timedelta
from app.microservices.task_tracker.src.routers.tasks_router import api_tasks_router

@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(api_tasks_router)
    return app

@pytest.mark.asyncio
async def test_create_and_get_task(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        task_data = {
            "title": "Test task",
            "description": "Some description",
            "status": "pending",
            "due_date": (datetime.utcnow() + timedelta(days=1)).isoformat()
        }

        create_response = await ac.post("/tasks", json=task_data)
        assert create_response.status_code == 200
        task = create_response.json()
        assert task["title"] == task_data["title"]
        assert "id" in task

        task_id = task["id"]
        get_response = await ac.get(f"/tasks/{task_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == task_id

@pytest.mark.asyncio
async def test_update_task(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        task_data = {
            "title": "Original",
            "description": "To update",
            "status": "pending",
            "due_date": datetime.utcnow().isoformat()
        }

        response = await ac.post("/tasks", json=task_data)
        task = response.json()
        task_id = task["id"]

        update_data = {
            "title": "Updated",
            "description": "Updated description",
            "status": "done",
            "due_date": datetime.utcnow().isoformat()
        }

        update_response = await ac.put(f"/tasks/{task_id}", json=update_data)
        assert update_response.status_code == 200
        updated = update_response.json()
        assert updated["title"] == "Updated"
        assert updated["status"] == "done"

@pytest.mark.asyncio
async def test_delete_task(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        task_data = {
            "title": "To be deleted",
            "description": "bye",
            "status": "pending",
            "due_date": datetime.utcnow().isoformat()
        }

        response = await ac.post("/tasks", json=task_data)
        task_id = response.json()["id"]

        delete_response = await ac.delete(f"/tasks/{task_id}")
        assert delete_response.status_code == 200

        get_response = await ac.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404
