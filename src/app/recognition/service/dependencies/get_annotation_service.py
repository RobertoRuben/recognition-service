from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from src.app.recognition.service.impl.annotation_service_impl import (
    AnnotationServiceImpl,
)
from src.app.recognition.service.interface.annotation_service import AnnotationService


def get_annotation_service() -> AnnotationService:
    return AnnotationServiceImpl()


AnnotationServiceDep = Annotated[AnnotationService, Depends(get_annotation_service)]
