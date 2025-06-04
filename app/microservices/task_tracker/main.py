from common.application import create_application
from src.routers.main_router import main_router


app = create_application()
app.include_router(main_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000, reload=True)