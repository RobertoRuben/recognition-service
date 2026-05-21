from __future__ import annotations

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from src.app.recognition.service.impl.embedding_service_impl import EmbeddingServiceImpl
from src.app.recognition.service.interface.embedding_service import EmbeddingService


@lru_cache(maxsize=1)
def _build() -> EmbeddingServiceImpl:
    return EmbeddingServiceImpl()


def get_embedding_service() -> EmbeddingService:
    return _build()


EmbeddingServiceDep = Annotated[EmbeddingService, Depends(get_embedding_service)]
