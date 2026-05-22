from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from src.app.common.db.dependencies.get_async_session import AsyncSessionDep
from src.app.employee.repository.employee_repository import EmployeeRepository
from src.app.employee.repository.face_embedding_repository import FaceEmbeddingRepository
from src.app.employee.service.impl.employee_service_impl import EmployeeServiceImpl
from src.app.employee.service.interface.employee_service import EmployeeService
from src.app.recognition.service.dependencies.get_embedding_service import (
    EmbeddingServiceDep,
)


def get_employee_repository(session: AsyncSessionDep) -> EmployeeRepository:
    return EmployeeRepository(session)


EmployeeRepositoryDep = Annotated[EmployeeRepository, Depends(get_employee_repository)]


def get_face_embedding_repository(session: AsyncSessionDep) -> FaceEmbeddingRepository:
    return FaceEmbeddingRepository(session)


FaceEmbeddingRepositoryDep = Annotated[
    FaceEmbeddingRepository, Depends(get_face_embedding_repository)
]


def get_employee_service(
    employee_repository: EmployeeRepositoryDep,
    face_embedding_repository: FaceEmbeddingRepositoryDep,
    embedding_service: EmbeddingServiceDep,
) -> EmployeeService:
    return EmployeeServiceImpl(
        employee_repository,
        face_embedding_repository,
        embedding_service,
    )


EmployeeServiceDep = Annotated[EmployeeService, Depends(get_employee_service)]
