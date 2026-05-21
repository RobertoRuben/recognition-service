from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EmployeeResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Internal employee ID.", example=1)
    dni: str = Field(
        description="Peruvian national ID — 8 numeric digits.", example="12345678"
    )
    name: str = Field(description="Employee first name(s).", example="Juan Carlos")
    paternal_surname: str = Field(
        description="Employee paternal surname.", example="García"
    )
    maternal_surname: str = Field(
        description="Employee maternal surname.", example="López"
    )
    created_at: datetime = Field(
        description="Timestamp when the record was created.",
        example="2024-01-15T10:30:00",
    )
    updated_at: datetime = Field(
        description="Timestamp of the last update.", example="2024-01-15T10:30:00"
    )
