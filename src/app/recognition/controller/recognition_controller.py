from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, File, Form, Query, Response, UploadFile, status
from pydantic import WithJsonSchema

from src.app.recognition.dto.response.face_count_result import FaceCountResult
from src.app.recognition.dto.response.face_match import FaceMatch
from src.app.recognition.dto.response.multi_face_identification_result import (
    MultiFaceIdentificationResult,
)
from src.app.recognition.dto.response.verification_result_dto import VerificationResultDTO
from src.app.recognition.service.dependencies.get_embedding_service import (
    EmbeddingServiceDep,
)
from src.app.recognition.service.dependencies.get_face_identification_service import (
    FaceIdentificationServiceDep,
)


_UploadFile = Annotated[UploadFile, WithJsonSchema({"type": "string", "format": "binary"})]


router = APIRouter(prefix="/recognition", tags=["Recognition"])


@router.post(
    "/identify",
    response_model=list[FaceMatch],
    status_code=status.HTTP_200_OK,
    summary="Identify a face",
    description="Matches a single-face photo against registered employees and returns the top `limit` results ranked by similarity. The photo must contain exactly one face.",
)
async def identify(
    service: FaceIdentificationServiceDep,
    photo: Annotated[_UploadFile, File(description="Single-face photo to identify")],
    limit: Annotated[int | None, Query(ge=1, le=20)] = None,
) -> list[FaceMatch]:
    image_bytes = await photo.read()
    return await service.identify(image_bytes, limit)


@router.post(
    "/identify-all",
    response_model=MultiFaceIdentificationResult,
    status_code=status.HTTP_200_OK,
    summary="Identify all faces",
    description="Detects every face in the image and independently matches each one against registered employees.",
)
async def identify_all(
    service: FaceIdentificationServiceDep,
    photo: Annotated[_UploadFile, File(description="Image with one or more faces to identify")],
    limit: Annotated[int | None, Query(ge=1, le=20)] = None,
) -> MultiFaceIdentificationResult:
    image_bytes = await photo.read()
    return await service.identify_all(image_bytes, limit)


@router.post(
    "/count",
    response_model=FaceCountResult,
    status_code=status.HTTP_200_OK,
    summary="Count faces in an image",
    description="Returns the number of faces detected in the image. Does not perform any identification.",
)
async def count_faces(
    service: EmbeddingServiceDep,
    photo: Annotated[_UploadFile, File(description="Image to count faces in")],
) -> FaceCountResult:
    image_bytes = await photo.read()
    total = await service.count_faces(image_bytes)
    return FaceCountResult(total_faces=total)


@router.post(
    "/annotate",
    status_code=status.HTTP_200_OK,
    summary="Annotate faces with bounding boxes",
    description="Returns the original image with a bounding box drawn around each detected face. Response is a JPEG image.",
    responses={200: {"content": {"image/jpeg": {}}, "description": "JPEG image with bounding boxes drawn around detected faces"}},
)
async def annotate(
    service: FaceIdentificationServiceDep,
    photo: Annotated[_UploadFile, File(description="Image to annotate with detected faces")],
) -> Response:
    image_bytes = await photo.read()
    annotated = await service.annotate(image_bytes)
    return Response(content=annotated, media_type="image/jpeg")


@router.post(
    "/verify",
    response_model=VerificationResultDTO,
    status_code=status.HTTP_200_OK,
    summary="Verify a face against a specific employee",
    description="Checks whether the face in the photo matches the registered embeddings of the employee identified by the given DNI (1:1 verification). Returns the best similarity found. Raises 404 if the employee is not found, has no embeddings, or if the face does not meet the similarity threshold.",
)
async def verify(
    service: FaceIdentificationServiceDep,
    dni: Annotated[
        str,
        Form(
            min_length=8,
            max_length=8,
            pattern=r"^\d{8}$",
            description="DNI of the employee to verify against (8 numeric digits).",
        ),
    ],
    photo: Annotated[_UploadFile, File(description="Single-face photo to verify")],
) -> VerificationResultDTO:
    image_bytes = await photo.read()
    return await service.verify(dni, image_bytes)
