from fastapi import APIRouter

from psycho_navigator.config import get_settings
from psycho_navigator.data.health import SettingsDict

router = APIRouter(prefix="/health", tags=["health"])
settings = get_settings()


@router.get("/")
async def get_health() -> SettingsDict:
    return settings.model_dump()
