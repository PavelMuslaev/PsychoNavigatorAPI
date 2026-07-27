from fastapi import FastAPI, APIRouter
from psycho_navigator.config import get_settings, Settings
from psycho_navigator.api.routers import get_router


def create_app(settings: Settings, *routers: APIRouter) -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )
    for router in routers:
        application.include_router(router)
    return application


app = create_app(get_settings(), get_router())
