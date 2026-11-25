from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from psycho_navigator.handlers.scoring import load_bfi2_key
from psycho_navigator.config import get_settings, Settings
from psycho_navigator.api.routers import get_router
from psycho_navigator.handlers.tests.questionnaires import load_questionnaires


def create_app(settings: Settings, *routers: APIRouter) -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        application.state.questionnaires = load_questionnaires(settings.path_dir_tests)

        application.state.bfi2_key = load_bfi2_key(
            settings.scoring_key_path, application.state.questionnaires
        )
        yield

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )
    for router in routers:
        application.include_router(router)
    return application


app = create_app(get_settings(), get_router())
