from __future__ import annotations

from typing import Protocol

from src.app.recognition.dto.response.face_match import FaceMatch


class FaceRecognitionService(Protocol):
    async def match_one(
        self, embedding: list[float], limit: int
    ) -> list[FaceMatch]: ...
