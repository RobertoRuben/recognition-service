from __future__ import annotations

from src.app.common.db.decorator.transactional import transactional
from src.app.common.exception import ConflictException, NotFoundException
from src.app.common.pagination.paginated import Paginated
from src.app.common.pagination.pagination_meta import PaginationMeta
from src.app.plan.dto.request.plan_activation_request_dto import PlanActivationRequestDTO
from src.app.plan.dto.request.plan_create_request_dto import PlanCreateRequestDTO
from src.app.plan.dto.request.plan_update_request_dto import PlanUpdateRequestDTO
from src.app.plan.dto.response.plan_response_dto import PlanResponseDTO
from src.app.plan.model.plan import Plan
from src.app.plan.repository.plan_repository import PlanRepository


class PlanServiceImpl:
    __session_attr__ = "plan_repository.session"

    def __init__(self, plan_repository: PlanRepository) -> None:
        self.plan_repository = plan_repository

    @transactional
    async def create(self, dto: PlanCreateRequestDTO) -> PlanResponseDTO:
        if await self.plan_repository.exist_by(Plan.name, dto.name):
            raise ConflictException(f"A plan with name '{dto.name}' already exists.")

        plan = Plan(**dto.model_dump())
        await self.plan_repository.save(plan)
        return PlanResponseDTO.model_validate(plan)

    @transactional(read_only=True)
    async def get_all(self) -> list[PlanResponseDTO]:
        plans = await self.plan_repository.get_all()
        return [PlanResponseDTO.model_validate(p) for p in plans]

    @transactional(read_only=True)
    async def list_paginated(self, page: int, size: int) -> Paginated[PlanResponseDTO]:
        items, total = await self.plan_repository.paginate(page, size)
        return Paginated[PlanResponseDTO](
            data=[PlanResponseDTO.model_validate(p) for p in items],
            pagination=PaginationMeta.build(page, size, total),
        )

    @transactional
    async def update(self, plan_id: int, dto: PlanUpdateRequestDTO) -> PlanResponseDTO:
        plan: Plan | None = await self.plan_repository.get_by_id(plan_id)

        if plan is None:
            raise NotFoundException(f"Plan with id {plan_id} not found.")

        new_name: str | None = dto.name
        if (
            new_name is not None
            and new_name != plan.name
            and await self.plan_repository.exist_by(Plan.name, new_name)
        ):
            raise ConflictException(f"A plan with name '{new_name}' already exists.")

        changes = dto.model_dump(exclude_unset=True)
        for field, value in changes.items():
            setattr(plan, field, value)

        updated = await self.plan_repository.save(plan)
        return PlanResponseDTO.model_validate(updated)

    @transactional
    async def set_activation(
        self, plan_id: int, dto: PlanActivationRequestDTO
    ) -> PlanResponseDTO:
        plan: Plan | None = await self.plan_repository.get_by_id(plan_id)

        if plan is None:
            raise NotFoundException(f"Plan with id {plan_id} not found.")

        plan.is_active = dto.is_active
        updated = await self.plan_repository.save(plan)
        return PlanResponseDTO.model_validate(updated)

    @transactional
    async def delete(self, plan_id: int) -> None:
        if not await self.plan_repository.exist_by(Plan.id, plan_id):
            raise NotFoundException(f"Plan with id {plan_id} not found.")
        await self.plan_repository.delete_by_id(plan_id)
