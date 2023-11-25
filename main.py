from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/healthychecker")
def read_root():
    return {"Hello": "World"}

