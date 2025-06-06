from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.orm import Session

from common.db import SessionLocal


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


SessionDep = Depends(get_session)
SessionAnnotatedDep = Annotated[Session, SessionDep]