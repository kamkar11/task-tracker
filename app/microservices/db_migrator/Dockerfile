FROM base-python:3.12.5

WORKDIR /app

COPY app/microservices/db_migrator/alembic.ini ./alembic.ini
COPY app/microservices/db_migrator/alembic ./alembic

CMD ["alembic", "upgrade", "head"]