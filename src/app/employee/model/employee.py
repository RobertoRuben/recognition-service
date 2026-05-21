from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.common.model import Base

if TYPE_CHECKING:
    from src.app.employee.model.face_embedding import FaceEmbedding


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    dni: Mapped[str] = mapped_column(String(8), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    paternal_surname: Mapped[str] = mapped_column(String(255), nullable=False)
    maternal_surname: Mapped[str] = mapped_column(String(255), nullable=False)

    face_embeddings: Mapped[list[FaceEmbedding]] = relationship(
        "FaceEmbedding",
        back_populates="employee",
        cascade="all, delete-orphan",
        lazy="select",
    )
