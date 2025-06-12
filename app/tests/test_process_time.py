import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from common.middleware.process_time import process_time_middleware

@pytest.fixture
def test_app():
    app = FastAPI()
    app.middleware("http")(process_time_middleware)

    @app.get("/test")
    async def read_test():
        return {"message": "ok"}

    return app

@pytest.mark.asyncio
async def test_process_time_header(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/test")

    assert response.status_code == 200
    assert "X-Process-Time" in response.headers
    assert float(response.headers["X-Process-Time"]) > 0