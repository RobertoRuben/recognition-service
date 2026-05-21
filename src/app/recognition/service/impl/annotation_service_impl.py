from __future__ import annotations

import asyncio

import cv2
import numpy as np

from src.app.common.exception import BadRequestException
from src.app.recognition.service.interface.annotation_service import FaceAnnotation

_FONT = cv2.FONT_HERSHEY_SIMPLEX
_WHITE = (255, 255, 255)
_BLACK = (0, 0, 0)
_GREEN = (0, 255, 0)


class AnnotationServiceImpl:
    def _run_draw(
        self, image_bytes: bytes, annotations: list[FaceAnnotation]
    ) -> bytes:
        arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise BadRequestException(
                "Could not decode image; ensure it is a valid JPEG or PNG."
            )

        for ann in annotations:
            x1, y1, x2, y2 = (int(v) for v in ann.bbox)
            cv2.rectangle(img, (x1, y1), (x2, y2), _GREEN, 2)
            if ann.label:
                cv2.putText(
                    img, ann.label, (x1 + 1, y1 - 5), _FONT, 0.55, _BLACK, 2, cv2.LINE_AA
                )
                cv2.putText(
                    img, ann.label, (x1, y1 - 6), _FONT, 0.55, _WHITE, 1, cv2.LINE_AA
                )

        total = f"Total faces: {len(annotations)}"
        cv2.putText(img, total, (11, 26), _FONT, 0.6, _BLACK, 2, cv2.LINE_AA)
        cv2.putText(img, total, (10, 25), _FONT, 0.6, _WHITE, 1, cv2.LINE_AA)

        ok, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 92])
        if not ok:
            raise BadRequestException("Failed to encode annotated image.")
        return buf.tobytes()

    async def draw(
        self, image_bytes: bytes, annotations: list[FaceAnnotation]
    ) -> bytes:
        return await asyncio.to_thread(self._run_draw, image_bytes, annotations)
