from typing import TypedDict
from typing import LiteralString, Literal


class SettingsDict(TypedDict):
    app_name: str
    app_version: str
    app_environment: Literal["local", "test", "production"]
    debug: bool
