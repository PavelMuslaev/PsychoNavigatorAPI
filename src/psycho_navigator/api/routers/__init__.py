from fastapi import APIRouter

from psycho_navigator.api.routers.tests import router as tests_router
from psycho_navigator.api.routers.health import router as health_router
from psycho_navigator.api.routers.history import router as history_router


def get_router() -> APIRouter:
    router = APIRouter()
    router.include_router(tests_router)
    router.include_router(health_router)
    router.include_router(history_router)

    return router
