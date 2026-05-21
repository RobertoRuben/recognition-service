from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.common.db.session import dispose_engine
from src.app.common.exception import (
    ProblemDetailsException,
    problem_details_exception_handler,
)
from src.app.employee.controller.employee_controller import router as employee_router
from src.app.recognition.controller.recognition_controller import router as recognition_router
from src.app.recognition.service.dependencies.get_embedding_service import (
    get_embedding_service,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    service = get_embedding_service()
    service.warmup()
    yield
    await dispose_engine()


app = FastAPI(
    swagger_ui_parameters={"displayRequestDuration": True},
    lifespan=lifespan
    )

app.add_exception_handler(ProblemDetailsException, problem_details_exception_handler)

app.include_router(employee_router)
app.include_router(recognition_router)

