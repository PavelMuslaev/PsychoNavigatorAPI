from fastapi import APIRouter, Depends

from psycho_navigator.config import get_settings, Settings
from psycho_navigator.schemas.health import HealthResponse
from typing import Annotated

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=HealthResponse)
async def get_health(
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    return HealthResponse(
        status="ok", version=settings.app_version, environment=settings.app_environment
    )
