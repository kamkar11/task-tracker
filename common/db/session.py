from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from common.settings import settings

engine = create_engine(str(settings.DATABASE_URI))
SessionLocal = sessionmaker(autoflush=True, bind=engine)