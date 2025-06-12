from fastapi import FastAPI

from common.application.health_router import health_router
from common.middleware.process_time import process_time_middleware


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(health_router)
    application.middleware('http')(process_time_middleware)

    return application