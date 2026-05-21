from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FaceMatch(BaseModel):
    dni: str = Field(description="DNI of the matched employee.", example="12345678")
    name: str = Field(description="First name(s) of the matched employee.", example="Juan Carlos")
    paternal_surname: str = Field(description="Paternal surname of the matched employee.", example="García")
    maternal_surname: str = Field(description="Maternal surname of the matched employee.", example="López")
    similarity: float = Field(ge=0.0, le=100.0, description="Match confidence as a percentage (0–100).", example=87.5)
    model_config = ConfigDict(from_attributes=True)
