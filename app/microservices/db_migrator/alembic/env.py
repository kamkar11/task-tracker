from alembic import context
from sqlalchemy import engine_from_config

from common.db import Base
from common.settings.settings import settings

config = context.config

def run_migrations_offline():
    context.configure(
        url=str(settings.DATABASE_URI)
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
