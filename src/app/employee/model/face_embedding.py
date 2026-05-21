from __future__ import annotations

from typing import TYPE_CHECKING

from pgvector.sqlalchemy import VECTOR
from sqlalchemy import BigInteger, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.common.model import Base

if TYPE_CHECKING:
    from src.app.employee.model.employee import Employee

EMBEDDING_DIM = 512


class FaceEmbedding(Base):
    __tablename__ = "face_embeddings"

    __table_args__ = (
        Index(
            "ix_face_embeddings_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    embedding: Mapped[list[float]] = mapped_column(
        VECTOR(EMBEDDING_DIM), nullable=False
    )

    employee: Mapped[Employee] = relationship(
        "Employee",
        back_populates="face_embeddings",
    )
