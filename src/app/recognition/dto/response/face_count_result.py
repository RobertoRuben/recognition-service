from __future__ import annotations

from pydantic import BaseModel, Field


class FaceCountResult(BaseModel):
    total_faces: int = Field(description="Number of faces detected in the image.", example=2)
