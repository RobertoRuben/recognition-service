from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FaceEmbeddingResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Face embedding ID.", example=1)
    employee_id: int = Field(
        description="ID of the employee this embedding belongs to.", example=1
    )
    created_at: datetime = Field(
        description="Timestamp when the embedding was registered.",
        example="2024-01-15T10:30:00",
    )
