from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.config import settings
from app.database import Base

# Import all models so Alembic sees them
from app.auth.models import User  # noqa: F401
from app.conversations.models import Conversation, Message  # noqa: F401
from app.tasks.models import Task, Goal, Habit, HabitLog, CalendarEvent  # noqa: F401
from app.memory.models import Memory, Note  # noqa: F401
from app.fitness.models import Workout, WeightLog, WaterLog, SleepLog  # noqa: F401
from app.finance.models import Expense, Budget, SavingsGoal  # noqa: F401
from app.study.models import StudyPlan, StudySession  # noqa: F401
from app.devices.models import Device, DeviceReading, Automation  # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
