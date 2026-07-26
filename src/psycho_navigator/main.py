from fastapi import FastAPI
from psycho_navigator.config import get_settings, Settings
from psycho_navigator.api.routers import get_router


def create_app(setting: Settings, *routers) -> FastAPI:
    app = FastAPI(**setting.model_dump())
    for i in routers:
        app.include_router(i)
    return app


app = create_app(get_settings(), get_router())
