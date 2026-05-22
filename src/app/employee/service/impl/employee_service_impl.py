from __future__ import annotations

from fastapi import UploadFile

from src.app.common.db.decorator.transactional import transactional
from src.app.common.exception import (
    BadRequestException,
    ConflictException,
    InvalidParametersException,
    NotFoundException,
)
from src.app.common.exception.exception_rfc_schema import InvalidParam
from src.app.common.pagination.paginated import Paginated
from src.app.common.pagination.pagination_meta import PaginationMeta
from src.app.employee.dto.request.employee_create_dto import EmployeeCreateRequestDTO
from src.app.employee.dto.request.employee_update_dto import EmployeeUpdateRequestDTO
from src.app.employee.dto.response.employee_response_dto import EmployeeResponseDTO
from src.app.employee.dto.response.employee_with_embeddings_dto import (
    EmployeeWithEmbeddingsResponseDTO,
)
from src.app.employee.dto.response.face_embedding_response_dto import (
    FaceEmbeddingResponseDTO,
)
from src.app.employee.model.employee import Employee
from src.app.employee.model.face_embedding import FaceEmbedding
from src.app.employee.repository.employee_repository import EmployeeRepository
from src.app.employee.repository.face_embedding_repository import (
    FaceEmbeddingRepository,
)
from src.app.recognition.service.interface.embedding_service import EmbeddingService


class EmployeeServiceImpl:
    __session_attr__ = "employee_repository.session"

    def __init__(
        self,
        employee_repository: EmployeeRepository,
        face_embedding_repository: FaceEmbeddingRepository,
        embedding_service: EmbeddingService,
    ) -> None:
        self.employee_repository: EmployeeRepository = employee_repository
        self.face_embedding_repository: FaceEmbeddingRepository = face_embedding_repository
        self.embedding_service: EmbeddingService = embedding_service

    @transactional
    async def create(
        self,
        employee_request_dto: EmployeeCreateRequestDTO,
        photos: list[UploadFile],
    ) -> EmployeeWithEmbeddingsResponseDTO:
        if not photos:
            raise BadRequestException("At least one photo is required.")

        if await self.employee_repository.exist_by(Employee.dni, employee_request_dto.dni):
            raise ConflictException(
                f"An employee with DNI '{employee_request_dto.dni}' already exists."
            )

        employee = Employee(
            dni=employee_request_dto.dni,
            name=employee_request_dto.name,
            paternal_surname=employee_request_dto.paternal_surname,
            maternal_surname=employee_request_dto.maternal_surname,
        )
        await self.employee_repository.save(employee)

        images: list[bytes] = [await photo.read() for photo in photos]
        vectors: list[list[int | float]] = await self.embedding_service.extract_embeddings_batch(images)

        await self.face_embedding_repository.bulk_save(
            [
                FaceEmbedding(employee_id=employee.id, embedding=vector)
                for vector in vectors
            ]
        )

        await self.employee_repository.session.refresh(employee, attribute_names=["face_embeddings"])
        return EmployeeWithEmbeddingsResponseDTO.model_validate(employee)

    @transactional
    async def update(
        self,
        employee_id: int,
        employee_request_dto: EmployeeUpdateRequestDTO,
    ) -> EmployeeResponseDTO:
        model: Employee | None = await self.employee_repository.get_by_id(employee_id)

        if model is None:
            raise NotFoundException(f"Employee with id {employee_id} not found.")

        entity = Employee.model_validate(model)

        new_dni: str | None = employee_request_dto.dni

        if (
            new_dni is not None
            and new_dni != entity.dni
            and await self.employee_repository.exist_by(
                Employee.dni,
                new_dni,
            )
        ):
            raise ConflictException(f"An employee with DNI '{new_dni}' already exists.")

        changes = employee_request_dto.model_dump(exclude_unset=True)

        for field, value in changes.items():
            setattr(entity, field, value)

        updated_model = await self.employee_repository.save(entity)

        return EmployeeResponseDTO.model_validate(updated_model)

    @transactional(read_only=True)
    async def get_by_id(self, employee_id: int) -> EmployeeWithEmbeddingsResponseDTO:
        employee: Employee | None = await self.employee_repository.find_by_id_with_embeddings(
            employee_id
        )
        if not employee:
            raise NotFoundException(f"Employee with id {employee_id} not found.")
        return EmployeeWithEmbeddingsResponseDTO.model_validate(employee)

    @transactional(read_only=True)
    async def get_by_dni(self, dni: str) -> EmployeeWithEmbeddingsResponseDTO:
        employee = await self.employee_repository.find_by_dni_with_embeddings(dni)
        if not employee:
            raise NotFoundException(f"Employee with DNI '{dni}' not found.")
        return EmployeeWithEmbeddingsResponseDTO.model_validate(employee)

    @transactional(read_only=True)
    async def list_paginated(
        self, page: int, size: int
    ) -> Paginated[EmployeeResponseDTO]:
        items, total = await self.employee_repository.paginate(page, size)
        return Paginated[EmployeeResponseDTO](
            data=[EmployeeResponseDTO.model_validate(e) for e in items],
            pagination=PaginationMeta.build(page, size, total),
        )

    @transactional
    async def delete(self, employee_id: int) -> None:
        if not await self.employee_repository.exist_by(Employee.id, employee_id):
            raise NotFoundException(f"Employee with id {employee_id} not found.")
        await self.employee_repository.delete_by_id(employee_id)

    @transactional
    async def add_photos(
        self,
        employee_id: int,
        photos: list[UploadFile],
    ) -> list[FaceEmbeddingResponseDTO]:
        if not photos:
            raise BadRequestException("At least one photo is required.")

        if not await self.employee_repository.exist_by(Employee.id, employee_id):
            raise NotFoundException(f"Employee with id {employee_id} not found.")

        images: list[bytes] = [await photo.read() for photo in photos]
        vectors: list[list[int | float]] = await self.embedding_service.extract_embeddings_batch(images)

        new_embeddings: list[FaceEmbedding] = [
            FaceEmbedding(employee_id=employee_id, embedding=vector)
            for vector in vectors
        ]
        await self.face_embedding_repository.bulk_save(new_embeddings)

        return [FaceEmbeddingResponseDTO.model_validate(fe) for fe in new_embeddings]

    @transactional
    async def delete_photos(self, employee_id: int, photo_ids: list[int]) -> None:
        if not await self.employee_repository.exist_by(Employee.id, employee_id):
            raise NotFoundException(f"Employee with id {employee_id} not found.")

        found_ids = await self.face_embedding_repository.find_existing_ids_for_employee(
            employee_id, photo_ids
        )

        if missing := [pid for pid in photo_ids if pid not in found_ids]:
            raise InvalidParametersException(
                detail="Some photo IDs do not belong to this employee.",
                invalid_params=[
                    InvalidParam(
                        name="photo_ids",
                        reason=f"ID {pid} not found for this employee.",
                    )
                    for pid in missing
                ],
            )

        await self.face_embedding_repository.bulk_delete(photo_ids)
