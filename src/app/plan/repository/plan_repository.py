from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.repository.impl.generic_repository_impl import GenericRepositoryImpl
from src.app.plan.model.plan import Plan


class PlanRepository(GenericRepositoryImpl[Plan]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Plan, session)
