from __future__ import annotations

from pydantic import BaseModel, Field


class VerificationResultDTO(BaseModel):
    verified: bool = Field(
        description="True if the photo's face matches the registered embeddings of the given DNI above the configured threshold.",
        example=True,
    )
    similarity: float = Field(
        ge=0.0,
        le=100.0,
        description="Best similarity found against the employee's registered embeddings, as a percentage (0–100).",
        example=92.4,
    )
    dni: str = Field(
        description="DNI provided in the request (echoed back for client convenience).",
        example="12345678",
    )
