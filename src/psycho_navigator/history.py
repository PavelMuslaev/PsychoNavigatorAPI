from pathlib import Path

from sqlalchemy import (
    JSON,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
    URL,
)

metadata = MetaData()
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("telegram_user_id", Integer, nullable=False, unique=True),
)
attempts = Table(
    "test_attempts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("attempt_id", String, nullable=False),
    Column("test_code", String, nullable=False),
    Column("version", String, nullable=False),
    Column("test_name", String, nullable=False),
    Column("completed_at", String, nullable=False),
    Column("profile", JSON, nullable=False),
    UniqueConstraint("user_id", "attempt_id"),
)


def database_url(path: Path) -> URL:
    return URL.create("sqlite", database=str(path.resolve()))
