from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel

from src.app.common.pagination.pagination_meta import PaginationMeta

T = TypeVar("T")


class Paginated(BaseModel, Generic[T]):
    data: list[T]
    pagination: PaginationMeta
