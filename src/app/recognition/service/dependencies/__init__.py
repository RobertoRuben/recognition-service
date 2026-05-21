from .get_annotation_service import AnnotationServiceDep, get_annotation_service
from .get_embedding_service import EmbeddingServiceDep, get_embedding_service
from .get_face_identification_service import (
    FaceIdentificationServiceDep,
    get_face_identification_service,
)
from .get_face_recognition_service import (
    FaceRecognitionServiceDep,
    get_face_recognition_service,
)

__all__: list[str] = [
    "AnnotationServiceDep",
    "EmbeddingServiceDep",
    "FaceIdentificationServiceDep",
    "FaceRecognitionServiceDep",
    "get_annotation_service",
    "get_embedding_service",
    "get_face_identification_service",
    "get_face_recognition_service",
]
