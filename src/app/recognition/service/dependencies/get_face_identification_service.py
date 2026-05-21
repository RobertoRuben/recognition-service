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


def get_face_identification_service(
    session: AsyncSessionDep,
    embedding_service: EmbeddingServiceDep,
    face_recognition_service: FaceRecognitionServiceDep,
    annotation_service: AnnotationServiceDep,
) -> FaceIdentificationService:
    return FaceIdentificationServiceImpl(
        session,
        embedding_service,
        face_recognition_service,
        annotation_service,
        EmployeeRepository(session),
    )


FaceIdentificationServiceDep = Annotated[
    FaceIdentificationService, Depends(get_face_identification_service)
]
