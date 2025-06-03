from fastapi.responses import Response
from fastapi.routing import APIRouter

health_router = APIRouter(tags=["Health check"])

@health_router.get("/healthcheck")
async def get_ok_response() -> Response:
    return Response(status_code=200, content="OK")