from __future__ import annotations

import asyncio
import warnings

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from src.app.common.config.base_config import base_config
from src.app.common.exception import BadRequestException
from src.app.recognition.service.interface.embedding_service import DetectedFace

if not hasattr(np, "int"):
    np.int = int  # noqa: NPY201 — InsightFace 0.7.3 draw_on() still uses removed np.int

warnings.filterwarnings(
    "ignore",
    message=r"`estimate` is deprecated.*",
    category=FutureWarning,
    module=r"insightface\.utils\.face_align",
)


class EmbeddingServiceImpl:
    def __init__(self) -> None:
        self._model = FaceAnalysis(
            name="buffalo_l",
            providers=base_config.recognition_providers,
            allowed_modules=base_config.recognition_allowed_modules,
        )
        ctx_id = 0 if "CUDAExecutionProvider" in base_config.recognition_providers else -1
        size = base_config.recognition_det_size
        self._model.prepare(
            ctx_id=ctx_id,
            det_size=(size, size),
            det_thresh=base_config.recognition_det_thresh,
        )

    def warmup(self) -> None:
        size = base_config.recognition_det_size
        dummy = np.zeros((size, size, 3), dtype=np.uint8)
        self._model.get(dummy)

    def _decode_image(self, image_bytes: bytes) -> np.ndarray:
        arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise BadRequestException(
                "Could not decode image; ensure it is a valid JPEG or PNG."
            )
        return img

    def _detect(self, image_bytes: bytes):
        img = self._decode_image(image_bytes)
        return self._model.get(img)

    def _run_inference(self, image_bytes: bytes) -> list[float]:
        faces = self._detect(image_bytes)
        if len(faces) == 0:
            raise BadRequestException("No face detected in the image.")
        if len(faces) > 1:
            raise BadRequestException(
                "Multiple faces detected; provide a single-face image."
            )
        return faces[0].normed_embedding.tolist()

    def _run_detect_all(self, image_bytes: bytes) -> list[DetectedFace]:
        faces = self._detect(image_bytes)
        result: list[DetectedFace] = []
        for f in faces:
            x1, y1, x2, y2 = f.bbox
            result.append(
                DetectedFace(
                    bbox=(float(x1), float(y1), float(x2), float(y2)),
                    embedding=f.normed_embedding.tolist(),
                )
            )
        return result

    def _run_count(self, image_bytes: bytes) -> int:
        return len(self._detect(image_bytes))

    async def extract_embedding(self, image_bytes: bytes) -> list[float]:
        return await asyncio.to_thread(self._run_inference, image_bytes)

    async def extract_embeddings_batch(self, images: list[bytes]) -> list[list[float]]:
        results: list[list[float]] = []
        for image_bytes in images:
            results.append(await self.extract_embedding(image_bytes))
        return results

    async def detect_all_faces(self, image_bytes: bytes) -> list[DetectedFace]:
        return await asyncio.to_thread(self._run_detect_all, image_bytes)

    async def count_faces(self, image_bytes: bytes) -> int:
        return await asyncio.to_thread(self._run_count, image_bytes)
