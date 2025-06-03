from fastapi import FastAPI

from app.application.health_router import health_router


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(health_router)

    return application