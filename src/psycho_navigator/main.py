from fastapi import FastAPI, Path
from typing import Annotated
import json


app = FastAPI()

tests = [
    {"id": 1, "name": "Test is Nastya Loxic"},
    {"id": 2, "name": "Test is Bob Loxic"},
    {"id": 3, "name": "Test is Bob Loxic"},
    {"id": 4, "name": "Test is Tom Loxic"},
    {"id": 5, "name": "Test is Alice Loxic"},
]

@app.get("/test/{path_id}", tags=["test"])
async def root(path_id: Annotated[int, Path()]) -> dict[str, str | int] | None:
    for i in tests:
        if i["id"] == int(path_id):
            return i
    return None

