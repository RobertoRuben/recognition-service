from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from src.app.common.db.dependencies.get_async_session import AsyncSessionDep
from src.app.plan.repository.plan_repository import PlanRepository


def get_plan_repository(session: AsyncSessionDep) -> PlanRepository:
    return PlanRepository(session)


PlanRepositoryDep = Annotated[PlanRepository, Depends(get_plan_repository)]
