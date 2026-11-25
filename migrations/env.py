from alembic import context
from sqlalchemy import create_engine

from psycho_navigator.config import Settings
from psycho_navigator.history import database_url, metadata

url = database_url(Settings().database_path)
if context.is_offline_mode():
    context.configure(url=url, target_metadata=metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    with create_engine(url).begin() as connection:
        context.configure(connection=connection, target_metadata=metadata)
        context.run_migrations()
