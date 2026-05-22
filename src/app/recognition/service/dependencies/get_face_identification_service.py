from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from src.app.common.db.dependencies.get_async_session import AsyncSessionDep
from src.app.employee.repository.employee_repository import EmployeeRepository
from src.app.recognition.service.dependencies.get_annotation_service import (
    AnnotationServiceDep,
)
from src.app.recognition.service.dependencies.get_embedding_service import (
    EmbeddingServiceDep,
)
from src.app.recognition.service.dependencies.get_face_recognition_service import (
    FaceRecognitionServiceDep,
)
from src.app.recognition.service.impl.face_identification_service_impl import (
    FaceIdentificationServiceImpl,
)
from src.app.recognition.service.interface.face_identification_service import (
    FaceIdentificationService,
)


def get_employee_repository(session: AsyncSessionDep) -> EmployeeRepository:
    return EmployeeRepository(session)


EmployeeRepositoryDep = Annotated[EmployeeRepository, Depends(get_employee_repository)]


def get_face_identification_service(
    embedding_service: EmbeddingServiceDep,
    face_recognition_service: FaceRecognitionServiceDep,
    annotation_service: AnnotationServiceDep,
    employee_repository: EmployeeRepositoryDep,
) -> FaceIdentificationService:
    return FaceIdentificationServiceImpl(
        embedding_service,
        face_recognition_service,
        annotation_service,
        employee_repository,
    )


FaceIdentificationServiceDep = Annotated[
    FaceIdentificationService, Depends(get_face_identification_service)
]
