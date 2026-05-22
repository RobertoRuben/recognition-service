from __future__ import annotations

import asyncio

import numpy as np

from src.app.common.config.base_config import base_config
from src.app.common.db.decorator.transactional import transactional
from src.app.common.exception import NotFoundException
from src.app.employee.repository.employee_repository import EmployeeRepository
from src.app.recognition.dto.response.face_match import FaceMatch
from src.app.recognition.dto.response.multi_face_identification_result import (
    MultiFaceIdentificationResult,
)
from src.app.recognition.dto.response.verification_result_dto import VerificationResultDTO
from src.app.recognition.service.interface.annotation_service import (
    AnnotationService,
    FaceAnnotation,
)
from src.app.recognition.service.interface.embedding_service import EmbeddingService
from src.app.recognition.service.interface.face_recognition_service import (
    FaceRecognitionService,
)


class FaceIdentificationServiceImpl:
    __session_attr__ = "employee_repository.session"

    def __init__(
        self,
        embedding_service: EmbeddingService,
        face_recognition_service: FaceRecognitionService,
        annotation_service: AnnotationService,
        employee_repository: EmployeeRepository,
    ) -> None:
        self.embedding_service = embedding_service
        self.face_recognition_service = face_recognition_service
        self.annotation_service = annotation_service
        self.employee_repository = employee_repository

    @transactional(read_only=True)
    async def identify(
        self, image_bytes: bytes, limit: int | None = None
    ) -> list[FaceMatch]:
        embedding = await self.embedding_service.extract_embedding(image_bytes)
        effective_limit = min(max(limit or base_config.recognition_default_limit, 1), 20)
        matches = await self.face_recognition_service.match_one(embedding, effective_limit)
        if not matches:
            raise NotFoundException("No matching employee found.")
        return matches

    @transactional(read_only=True)
    async def identify_all(
        self, image_bytes: bytes, limit: int | None = None
    ) -> MultiFaceIdentificationResult:
        detected = await self.embedding_service.detect_all_faces(image_bytes)
        tops = await asyncio.gather(
            *(self.face_recognition_service.match_one(d.embedding, 1) for d in detected)
        )
        matches = [top[0] for top in tops if top]
        return MultiFaceIdentificationResult(total_faces=len(detected), matches=matches)

    @transactional(read_only=True)
    async def annotate(self, image_bytes: bytes) -> bytes:
        detected = await self.embedding_service.detect_all_faces(image_bytes)
        annotations = [FaceAnnotation(bbox=d.bbox, label=None) for d in detected]
        return await self.annotation_service.draw(image_bytes, annotations)

    @transactional(read_only=True)
    async def verify(self, dni: str, image_bytes: bytes) -> VerificationResultDTO:
        employee = await self.employee_repository.find_by_dni_with_embeddings(dni)
        if employee is None:
            raise NotFoundException(f"Employee with DNI '{dni}' not found.")
        if not employee.face_embeddings:
            raise NotFoundException(
                f"Employee with DNI '{dni}' has no registered face embeddings."
            )

        probe = np.asarray(
            await self.embedding_service.extract_embedding(image_bytes), dtype=np.float32
        )
        registered = np.asarray(
            [fe.embedding for fe in employee.face_embeddings], dtype=np.float32
        )
        # InsightFace embeddings are L2-normalised; dot product == cosine similarity.
        best_similarity = float((registered @ probe).max())
        best_distance = 1.0 - best_similarity

        if best_distance > base_config.recognition_min_similarity:
            raise NotFoundException(f"Face does not match employee with DNI '{dni}'.")

        similarity_pct = round(max(0.0, min(100.0, best_similarity * 100.0)), 2)
        return VerificationResultDTO(verified=True, similarity=similarity_pct, dni=dni)
