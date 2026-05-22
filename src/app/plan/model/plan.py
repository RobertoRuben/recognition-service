from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.app.common.model import Base


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    monthly_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    annual_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    face_limit: Mapped[int] = mapped_column(BigInteger, nullable=False)
    request_limit_per_month: Mapped[int] = mapped_column(BigInteger, nullable=False)
    extra_face_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    extra_request_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

