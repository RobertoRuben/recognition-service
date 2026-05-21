from __future__ import annotations

from typing import Protocol

from src.app.recognition.dto.response.face_match import FaceMatch
from src.app.recognition.dto.response.multi_face_identification_result import (
    MultiFaceIdentificationResult,
)
from src.app.recognition.dto.response.verification_result_dto import VerificationResultDTO


class FaceIdentificationService(Protocol):
    async def identify(
        self, image_bytes: bytes, limit: int | None = None
    ) -> list[FaceMatch]: ...
    async def identify_all(
        self, image_bytes: bytes, limit: int | None = None
    ) -> MultiFaceIdentificationResult: ...
    async def annotate(self, image_bytes: bytes) -> bytes: ...
    async def verify(self, dni: str, image_bytes: bytes) -> VerificationResultDTO: ...
