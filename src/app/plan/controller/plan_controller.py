from __future__ import annotations

from fastapi import APIRouter, status

from src.app.common.pagination.paginated import Paginated
from src.app.plan.dto.request.plan_activation_request_dto import PlanActivationRequestDTO
from src.app.plan.dto.request.plan_create_request_dto import PlanCreateRequestDTO
from src.app.plan.dto.request.plan_update_request_dto import PlanUpdateRequestDTO
from src.app.plan.dto.response.plan_response_dto import PlanResponseDTO
from src.app.plan.service.dependencies.get_plan_service import PlanServiceDep

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.post(
    "/",
    response_model=PlanResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create plan",
    description="Creates a new subscription plan. The plan name must be unique.",
)
async def create_plan(
    data: PlanCreateRequestDTO,
    service: PlanServiceDep,
) -> PlanResponseDTO:
    return await service.create(data)


@router.get(
    "/",
    response_model=list[PlanResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="List all plans",
    description="Returns all plans without pagination.",
)
async def list_all_plans(service: PlanServiceDep) -> list[PlanResponseDTO]:
    return await service.get_all()


@router.get(
    "/paginated",
    response_model=Paginated[PlanResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="List plans paginated",
    description="Returns a paginated list of plans. Use `page` and `size` to control pagination.",
)
async def list_plans_paginated(
    service: PlanServiceDep,
    page: int = 1,
    size: int = 20,
) -> Paginated[PlanResponseDTO]:
    return await service.list_paginated(page, size)


@router.patch(
    "/{plan_id}",
    response_model=PlanResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Update plan",
    description="Partially updates plan fields. Only the fields included in the request body are modified.",
)
async def update_plan(
    plan_id: int,
    data: PlanUpdateRequestDTO,
    service: PlanServiceDep,
) -> PlanResponseDTO:
    return await service.update(plan_id, data)


@router.patch(
    "/{plan_id}/activation",
    response_model=PlanResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Activate or deactivate plan",
    description="Sets the active status of a plan. Use `is_active: true` to activate and `is_active: false` to deactivate.",
)
async def set_plan_activation(
    plan_id: int,
    data: PlanActivationRequestDTO,
    service: PlanServiceDep,
) -> PlanResponseDTO:
    return await service.set_activation(plan_id, data)


@router.delete(
    "/{plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete plan",
    description="Permanently deletes a plan by its ID.",
)
async def delete_plan(
    plan_id: int,
    service: PlanServiceDep,
) -> None:
    await service.delete(plan_id)
