from __future__ import annotations

from pydantic import BaseModel, Field


class EmployeeUpdateRequestDTO(BaseModel):
    dni: str | None = Field(
        default=None,
        min_length=8,
        max_length=8,
        pattern=r"^\d{8}$",
        description="Peruvian national ID — exactly 8 numeric digits.",
        example="12345678",
    )
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Employee first name(s).",
        example="Juan Carlos",
    )
    paternal_surname: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Employee paternal surname.",
        example="García",
    )
    maternal_surname: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Employee maternal surname.",
        example="López",
    )
