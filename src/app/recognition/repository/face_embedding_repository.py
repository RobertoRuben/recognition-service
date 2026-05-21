from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.repository.impl.generic_repository_impl import GenericRepositoryImpl
from src.app.employee.model.employee import Employee
from src.app.employee.model.face_embedding import FaceEmbedding


class FaceEmbeddingRepository(GenericRepositoryImpl[FaceEmbedding]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(FaceEmbedding, session)

    async def find_matches_by_embedding(
        self,
        embedding: list[float],
        max_distance: float,
        limit: int,
    ) -> list[dict]:
        distance = FaceEmbedding.embedding.cosine_distance(embedding).label("distance")
        inner = (
            select(
                Employee.dni,
                Employee.name,
                Employee.paternal_surname,
                Employee.maternal_surname,
                distance,
            )
            .join(FaceEmbedding, FaceEmbedding.employee_id == Employee.id)
            .where(distance <= max_distance)
            .order_by(Employee.id, distance)
            .distinct(Employee.id)
            .subquery()
        )
        final = select(inner).order_by(inner.c.distance).limit(limit)
        rows = (await self.session.execute(final)).mappings().all()
        return [dict(r) for r in rows]
