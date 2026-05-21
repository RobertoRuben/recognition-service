from __future__ import annotations

from pydantic import Field

from src.app.employee.dto.response.employee_response_dto import EmployeeResponseDTO
from src.app.employee.dto.response.face_embedding_response_dto import FaceEmbeddingResponseDTO


class EmployeeWithEmbeddingsResponseDTO(EmployeeResponseDTO):
    face_embeddings: list[FaceEmbeddingResponseDTO] = Field(
        description="Registered face embeddings for the employee.", example=[]
    )
