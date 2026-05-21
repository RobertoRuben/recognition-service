from __future__ import annotations

from typing import Protocol

from fastapi import UploadFile

from src.app.common.pagination.paginated import Paginated
from src.app.employee.dto.request.employee_create_dto import EmployeeCreateRequestDTO
from src.app.employee.dto.request.employee_update_dto import EmployeeUpdateRequestDTO
from src.app.employee.dto.response.employee_response_dto import EmployeeResponseDTO
from src.app.employee.dto.response.employee_with_embeddings_dto import (
    EmployeeWithEmbeddingsResponseDTO,
)
from src.app.employee.dto.response.face_embedding_response_dto import FaceEmbeddingResponseDTO


class EmployeeService(Protocol):
    async def create(
        self,
        employee_request_dto: EmployeeCreateRequestDTO,
        photos: list[UploadFile],
    ) -> EmployeeWithEmbeddingsResponseDTO: ...

    async def update(
        self,
        employee_id: int,
        employee_request_dto: EmployeeUpdateRequestDTO,
    ) -> EmployeeResponseDTO: ...

    async def get_by_id(
        self, employee_id: int
    ) -> EmployeeWithEmbeddingsResponseDTO: ...

    async def get_by_dni(self, dni: str) -> EmployeeWithEmbeddingsResponseDTO: ...

    async def list_paginated(
        self,
        page: int,
        size: int,
    ) -> Paginated[EmployeeResponseDTO]: ...

    async def delete(self, employee_id: int) -> None: ...

    async def add_photos(
        self,
        employee_id: int,
        photos: list[UploadFile],
    ) -> list[FaceEmbeddingResponseDTO]: ...

    async def delete_photos(
        self,
        employee_id: int,
        photo_ids: list[int],
    ) -> None: ...
