from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from src.app.common.db.dependencies.get_async_session import AsyncSessionDep
from src.app.recognition.repository.face_embedding_repository import FaceEmbeddingRepository
from src.app.recognition.service.impl.face_recognition_service_impl import (
    FaceRecognitionServiceImpl,
)
from src.app.recognition.service.interface.face_recognition_service import (
    FaceRecognitionService,
)


def get_face_recognition_service(session: AsyncSessionDep) -> FaceRecognitionService:
    return FaceRecognitionServiceImpl(FaceEmbeddingRepository(session))


FaceRecognitionServiceDep = Annotated[
    FaceRecognitionService, Depends(get_face_recognition_service)
]
