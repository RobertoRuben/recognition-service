from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from src.app.common.db.dependencies.get_async_session import AsyncSessionDep
from src.app.plan.repository.plan_repository import PlanRepository
from src.app.plan.service.impl.plan_service_impl import PlanServiceImpl
from src.app.plan.service.interface.plan_service import PlanService


def get_plan_repository(session: AsyncSessionDep) -> PlanRepository:
    return PlanRepository(session)


PlanRepositoryDep = Annotated[PlanRepository, Depends(get_plan_repository)]


def get_plan_service(plan_repository: PlanRepositoryDep) -> PlanService:
    return PlanServiceImpl(plan_repository)


PlanServiceDep = Annotated[PlanService, Depends(get_plan_service)]
