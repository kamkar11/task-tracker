FROM base-python:3.12.5

COPY ./alembic ./alembic
COPY ./alembic.ini ./alembic.ini

CMD ["alembic", "upgrade", "head"]