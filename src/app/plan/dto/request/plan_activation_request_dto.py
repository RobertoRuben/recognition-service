from pydantic import BaseModel, Field


class PlanActivationRequestDTO(BaseModel):
    is_active: bool = Field(
        ...,
        description="Whether the plan should be active.",
        examples=[True],
    )
