from fastapi import FastAPI, APIRouter
from psycho_navigator.config import get_settings, Settings
from psycho_navigator.api.routers import get_router


def create_app(setting: Settings, *routers: APIRouter) -> FastAPI:
    application = FastAPI(
        title=setting.app_name,
        version=setting.app_version,
        debug=setting.debug,
    )
    for i in routers:
        application.include_router(i)
    return application


app = create_app(get_settings(), get_router())
