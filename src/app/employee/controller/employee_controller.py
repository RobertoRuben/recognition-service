from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from pydantic import BaseModel, WithJsonSchema

from src.app.common.pagination.paginated import Paginated
from src.app.employee.dto.request import (
    EmployeeCreateRequestDTO,
    EmployeeUpdateRequestDTO,
)
from src.app.employee.dto.response import (
    EmployeeResponseDTO,
    EmployeeWithEmbeddingsResponseDTO,
    FaceEmbeddingResponseDTO,
)
from src.app.employee.service.dependencies.get_employee_service import (
    EmployeeServiceDep,
)

_UploadFile = Annotated[
    UploadFile, WithJsonSchema({"type": "string", "format": "binary"})
]


class DeletePhotosBody(BaseModel):
    photo_ids: list[int]


router = APIRouter(prefix="/employees", tags=["Employees"])


async def _employee_create_form(
    dni: str = Form(..., min_length=8, max_length=8, pattern=r"^\d{8}$"),
    name: str = Form(..., min_length=1, max_length=255),
    paternal_surname: str = Form(..., min_length=1, max_length=255),
    maternal_surname: str = Form(..., min_length=1, max_length=255),
) -> EmployeeCreateRequestDTO:
    return EmployeeCreateRequestDTO(
        dni=dni,
        name=name,
        paternal_surname=paternal_surname,
        maternal_surname=maternal_surname,
    )


@router.post(
    "/",
    response_model=EmployeeWithEmbeddingsResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create employee with photos",
    description="Registers a new employee and generates face embeddings from one or more photos. Each photo must contain exactly one face.",
)
async def create_employee(
    service: EmployeeServiceDep,
    data: Annotated[EmployeeCreateRequestDTO, Depends(_employee_create_form)],
    photos: Annotated[list[_UploadFile], File(description="Employee face photos")],
) -> EmployeeWithEmbeddingsResponseDTO:
    return await service.create(data, photos)


@router.get(
    "/",
    response_model=Paginated[EmployeeResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="List employees",
    description="Returns a paginated list of employees. Use `page` and `size` to control pagination.",
)
async def list_employees(
    service: EmployeeServiceDep,
    page: int = 1,
    size: int = 20,
) -> Paginated[EmployeeResponseDTO]:
    return await service.list_paginated(page, size)


@router.get(
    "/dni/{dni}",
    response_model=EmployeeWithEmbeddingsResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get employee by DNI",
    description="Returns the employee and their registered face embeddings. DNI must be exactly 8 numeric digits.",
)
async def get_employee_by_dni(
    dni: str,
    service: EmployeeServiceDep,
) -> EmployeeWithEmbeddingsResponseDTO:
    return await service.get_by_dni(dni)


@router.get(
    "/{employee_id}",
    response_model=EmployeeWithEmbeddingsResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get employee by ID",
    description="Returns the employee and their registered face embeddings.",
)
async def get_employee_by_id(
    employee_id: int,
    service: EmployeeServiceDep,
) -> EmployeeWithEmbeddingsResponseDTO:
    return await service.get_by_id(employee_id)


@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Update employee",
    description="Partially updates employee fields. Only the fields included in the request body are modified.",
)
async def update_employee(
    employee_id: int,
    data: EmployeeUpdateRequestDTO,
    service: EmployeeServiceDep,
) -> EmployeeResponseDTO:
    return await service.update(employee_id, data)


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete employee",
    description="Deletes the employee and all their associated face embeddings.",
)
async def delete_employee(
    employee_id: int,
    service: EmployeeServiceDep,
) -> None:
    await service.delete(employee_id)


@router.post(
    "/{employee_id}/photos",
    response_model=list[FaceEmbeddingResponseDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Add photos to employee",
    description="Generates additional face embeddings for the employee from new photos. Each photo must contain exactly one face.",
)
async def add_photos(
    employee_id: int,
    photos: Annotated[list[_UploadFile], File(description="Face photos to add")],
    service: EmployeeServiceDep,
) -> list[FaceEmbeddingResponseDTO]:
    return await service.add_photos(employee_id, photos)


@router.delete(
    "/{employee_id}/photos",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete employee photos",
    description="Removes specific face embeddings by their IDs. Useful when a registered photo no longer represents the employee.",
)
async def delete_photos(
    employee_id: int,
    body: DeletePhotosBody,
    service: EmployeeServiceDep,
) -> None:
    await service.delete_photos(employee_id, body.photo_ids)
