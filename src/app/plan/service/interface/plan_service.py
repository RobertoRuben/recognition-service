from __future__ import annotations

from typing import Protocol

from src.app.common.pagination.paginated import Paginated
from src.app.plan.dto.request.plan_activation_request_dto import PlanActivationRequestDTO
from src.app.plan.dto.request.plan_create_request_dto import PlanCreateRequestDTO
from src.app.plan.dto.request.plan_update_request_dto import PlanUpdateRequestDTO
from src.app.plan.dto.response.plan_response_dto import PlanResponseDTO


class PlanService(Protocol):
    async def create(self, dto: PlanCreateRequestDTO) -> PlanResponseDTO: ...

    async def get_all(self) -> list[PlanResponseDTO]: ...

    async def list_paginated(self, page: int, size: int) -> Paginated[PlanResponseDTO]: ...

    async def update(self, plan_id: int, dto: PlanUpdateRequestDTO) -> PlanResponseDTO: ...

    async def set_activation(
        self, plan_id: int, dto: PlanActivationRequestDTO
    ) -> PlanResponseDTO: ...

    async def delete(self, plan_id: int) -> None: ...
