from fastapi import FastAPI
from psycho_navigator.api.routers.tests import router as tests_router

app = FastAPI()
app.include_router(tests_router)
