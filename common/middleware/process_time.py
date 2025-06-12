import time
import logging
from fastapi import Request
from fastapi.responses import Response

logger = logging.getLogger(__name__)

async def process_time_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = time.perf_counter() - start_time

    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    logger.info(f"{request.method} {request.url.path} took {process_time:.6f}s")

    return response