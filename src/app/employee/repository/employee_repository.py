from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.common.repository.impl.generic_repository_impl import GenericRepositoryImpl
from src.app.employee.model.employee import Employee


class EmployeeRepository(GenericRepositoryImpl[Employee]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Employee, session)

    async def find_by_id_with_embeddings(self, employee_id: int) -> Employee | None:
        stmt = (
            select(Employee)
            .options(selectinload(Employee.face_embeddings))
            .where(Employee.id == employee_id)
        )
        return await self.session.scalar(stmt)

    async def find_by_dni_with_embeddings(self, dni: str) -> Employee | None:
        stmt = (
            select(Employee)
            .options(selectinload(Employee.face_embeddings))
            .where(Employee.dni == dni)
        )
        return await self.session.scalar(stmt)
