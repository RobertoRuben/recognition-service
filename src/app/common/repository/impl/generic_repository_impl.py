from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import delete, exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.app.common.model.base_model import Base

T = TypeVar("T", bound=Base)


class GenericRepositoryImpl(Generic[T]):
    def __init__(self, model: type[T], session: AsyncSession) -> None:
        self._model = model
        self.session = session

    async def save(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def get_all(self) -> list[T]:
        result = await self.session.execute(select(self._model))
        return list(result.scalars().all())

    async def count(self) -> int:
        total = await self.session.scalar(
            select(func.count()).select_from(self._model)
        )
        return total or 0

    async def get_by_id(self, id: int) -> T | None:
        return await self.session.get(self._model, id)

    async def get_by(self, attr: InstrumentedAttribute, value: Any) -> T | None:
        stmt = select(self._model).where(attr == value)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def find_all_by(self, attr: InstrumentedAttribute, value: Any) -> list[T]:
        stmt = select(self._model).where(attr == value)
        return list((await self.session.execute(stmt)).scalars().all())

    async def exist_by(self, attr: InstrumentedAttribute, value: Any) -> bool:
        stmt = select(exists().where(attr == value))
        return bool(await self.session.scalar(stmt))

    async def delete_by_id(self, id: int) -> None:
        entity = await self.session.get(self._model, id)
        if entity:
            await self.session.delete(entity)
            await self.session.flush()

    async def bulk_save(self, entities: list[T]) -> list[T]:
        self.session.add_all(entities)
        await self.session.flush()
        for entity in entities:
            await self.session.refresh(entity)
        return entities

    async def bulk_delete(self, ids: list[int]) -> None:
        await self.session.execute(
            delete(self._model).where(self._model.id.in_(ids))
        )
        await self.session.flush()

    async def paginate(self, page: int, size: int) -> tuple[list[T], int]:
        total = await self.session.scalar(
            select(func.count()).select_from(self._model)
        ) or 0
        stmt = (
            select(self._model)
            .order_by(self._model.id)
            .offset((page - 1) * size)
            .limit(size)
        )
        items = list((await self.session.execute(stmt)).scalars().all())
        return items, total
