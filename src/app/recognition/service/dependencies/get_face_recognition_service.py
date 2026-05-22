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


def get_recognition_face_embedding_repository(
    session: AsyncSessionDep,
) -> FaceEmbeddingRepository:
    return FaceEmbeddingRepository(session)


RecognitionFaceEmbeddingRepositoryDep = Annotated[
    FaceEmbeddingRepository, Depends(get_recognition_face_embedding_repository)
]


def get_face_recognition_service(
    repository: RecognitionFaceEmbeddingRepositoryDep,
) -> FaceRecognitionService:
    return FaceRecognitionServiceImpl(repository)


FaceRecognitionServiceDep = Annotated[
    FaceRecognitionService, Depends(get_face_recognition_service)
]
