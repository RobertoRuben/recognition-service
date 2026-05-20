from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.common.db.session import dispose_engine
from src.app.common.exception import (
    ProblemDetailsException,
    problem_details_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await dispose_engine()


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(ProblemDetailsException, problem_details_exception_handler)


@app.get("/")
def main():
    return {"message": "Hello World"}
