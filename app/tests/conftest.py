import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.microservices.task_tracker.src.routers.tasks_router import api_tasks_router
from common.db.models import Base
from common.dependencies.session import get_session

# Testowa baza SQLite in-memory
DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Tworzymy schematy przed testami i czyścimy po
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Sesja testowa dla każdego testu
@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(api_tasks_router)
    return app


@pytest.fixture(autouse=True)
def override_get_session(test_app, db_session):
    test_app.dependency_overrides[get_session] = lambda: db_session
