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


def get_employee_service(
    session: AsyncSessionDep,
    embedding_service: EmbeddingServiceDep,
) -> EmployeeService:
    employee_repo = EmployeeRepository(session)
    face_embedding_repo = FaceEmbeddingRepository(session)
    return EmployeeServiceImpl(session, employee_repo, face_embedding_repo, embedding_service)


EmployeeServiceDep = Annotated[EmployeeService, Depends(get_employee_service)]
