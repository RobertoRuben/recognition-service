from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class PlanCreateRequestDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="The name of the plan.",
        examples=["Basic Plan"],
    )

    description: str | None = Field(
        default=None,
        max_length=255,
        description="A brief description of the plan.",
        examples=["This plan offers basic features for small businesses."],
    )

    monthly_price: Decimal = Field(
        ...,
        gt=0,
        description="The monthly price of the plan in USD.",
        examples=[Decimal("9.99")],
    )

    annual_price: Decimal = Field(
        ...,
        gt=0,
        description="The annual price of the plan in USD.",
        examples=[Decimal("99.99")],
    )

    face_limit: int = Field(
        ...,
        ge=0,
        description="The maximum number of faces allowed under this plan.",
        examples=[1000],
    )

    request_limit_per_month: int = Field(
        ...,
        ge=0,
        description="The maximum number of requests allowed per month under this plan.",
        examples=[10000],
    )

    extra_face_price: Decimal = Field(
        ...,
        ge=0,
        description="The price for each additional face beyond the face limit in USD.",
        examples=[Decimal("0.10")],
    )

    extra_request_price: Decimal = Field(
        ...,
        ge=0,
        description="The price for each additional request beyond the monthly request limit in USD.",
        examples=[Decimal("0.01")],
    )