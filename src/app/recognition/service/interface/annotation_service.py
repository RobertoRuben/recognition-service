from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class FaceAnnotation:
    bbox: tuple[float, float, float, float]  # x1, y1, x2, y2
    label: str | None


class AnnotationService(Protocol):
    async def draw(
        self, image_bytes: bytes, annotations: list[FaceAnnotation]
    ) -> bytes: ...
