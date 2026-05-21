from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.repository.impl.generic_repository_impl import GenericRepositoryImpl
from src.app.employee.model.face_embedding import FaceEmbedding


class FaceEmbeddingRepository(GenericRepositoryImpl[FaceEmbedding]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(FaceEmbedding, session)

    async def find_existing_ids_for_employee(
        self, employee_id: int, photo_ids: list[int]
    ) -> set[int]:
        stmt = select(FaceEmbedding.id).where(
            FaceEmbedding.employee_id == employee_id,
            FaceEmbedding.id.in_(photo_ids),
        )
        rows = await self.session.scalars(stmt)
        return set(rows.all())
