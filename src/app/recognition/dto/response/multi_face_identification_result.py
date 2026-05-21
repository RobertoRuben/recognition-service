from __future__ import annotations

from pydantic import BaseModel, Field

from src.app.recognition.dto.response.face_match import FaceMatch


class MultiFaceIdentificationResult(BaseModel):
    total_faces: int = Field(description="Total number of faces detected in the image.", example=2)
    matches: list[FaceMatch] = Field(description="Best match for each detected face. Empty if no face exceeds the similarity threshold.", example=[])
