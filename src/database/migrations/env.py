from logging.config import fileConfig

from alembic import context
from alembic.config import Config
from sqlalchemy import engine_from_config, pool
from sqlalchemy.orm.decl_api import DeclarativeMeta

from src.database.models import Base
from src.utils.config import load_project_config, update_alembic_config


def run() -> None:
    config = context.config

    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    update_alembic_config(config, load_project_config().db_info)
    if context.is_offline_mode():
        run_migrations_offline(config, Base)
    else:
        run_migrations_online(config, Base)


def run_migrations_offline(config: Config, base: DeclarativeMeta) -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(config: Config, base: DeclarativeMeta) -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=base.metadata)

        with context.begin_transaction():
            context.run_migrations()


run()
