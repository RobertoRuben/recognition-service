from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class DetectedFace:
    bbox: tuple[float, float, float, float]  # x1, y1, x2, y2
    embedding: list[float]


class EmbeddingService(Protocol):
    def warmup(self) -> None: ...
    async def extract_embedding(self, image_bytes: bytes) -> list[float]: ...
    async def extract_embeddings_batch(
        self, images: list[bytes]
    ) -> list[list[float]]: ...
    async def detect_all_faces(self, image_bytes: bytes) -> list[DetectedFace]: ...
    async def count_faces(self, image_bytes: bytes) -> int: ...
