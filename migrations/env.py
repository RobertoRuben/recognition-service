import asyncio
import importlib
import pkgutil
from logging.config import fileConfig

from alembic import context

from src.app.common.model import Base
from src.app.common.db.session import engine
import src.app

# Alembic Config object, which provides access to the values within the .ini file.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata object for 'autogenerate' support.
target_metadata = Base.metadata


def import_models() -> None:
    """Imports all model modules so their classes register with Base.metadata."""
    for _, name, _ in pkgutil.walk_packages(
        src.app.__path__, src.app.__name__ + "."
    ):
        if name.endswith(".model") or ".model." in name:
            importlib.import_module(name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Configures the context with a URL. Calls to context.execute()
    here emit the string to the script output.
    """
    url = engine.url.render_as_string(hide_password=False)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Handles asynchronous connection and initiates the migration runner.

    Creates an AsyncConnection and uses run_sync to bridge the async
    engine with Alembic's synchronous requirements.
    """
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Initiates the asyncio event loop to execute the asynchronous migration flow.
    """
    asyncio.run(run_async_migrations())


# Entry point for Alembic execution.
import_models()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
