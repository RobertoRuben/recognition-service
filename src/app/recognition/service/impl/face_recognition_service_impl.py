from __future__ import annotations

from src.app.common.config.base_config import base_config
from src.app.recognition.dto.response.face_match import FaceMatch
from src.app.recognition.repository.face_embedding_repository import FaceEmbeddingRepository


class FaceRecognitionServiceImpl:
    def __init__(self, repository: FaceEmbeddingRepository) -> None:
        self.repository = repository

    async def match_one(self, embedding: list[float], limit: int) -> list[FaceMatch]:
        rows = await self.repository.find_matches_by_embedding(
            embedding, base_config.recognition_min_similarity, limit
        )
        return [
            FaceMatch(
                dni=r["dni"],
                name=r["name"],
                paternal_surname=r["paternal_surname"],
                maternal_surname=r["maternal_surname"],
                similarity=round(
                    max(0.0, min(100.0, (1.0 - float(r["distance"])) * 100.0)), 2
                ),
            )
            for r in rows
        ]
