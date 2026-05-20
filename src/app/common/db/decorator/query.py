from functools import wraps
from types import UnionType
from typing import Callable, Union, get_args, get_origin, get_type_hints

from pydantic import TypeAdapter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.exception import NotFoundException

_SCALAR_TYPES = (int, str, float, bool, bytes)


def query(sql: str):
    def decorator(f: Callable):
        return_type = get_type_hints(f).get("return")
        mode, adapter = _resolve(return_type)

        @wraps(f)
        async def wrapper(self, *args, **kwargs):
            session: AsyncSession = self.session
            result = await session.execute(text(sql), kwargs)

            if mode == "none":
                return None
            if mode == "scalar":
                return result.scalar_one_or_none()
            if mode == "list":
                return adapter.validate_python(result.mappings().all())

            row = result.mappings().first()
            if row is None:
                if mode == "single_required":
                    raise NotFoundException(f"No row returned by '{f.__name__}'")
                return None
            return adapter.validate_python(dict(row))

        return wrapper

    return decorator


def _resolve(return_type) -> tuple[str, TypeAdapter | None]:
    if return_type is None or return_type is type(None):
        return "none", None

    origin = get_origin(return_type)

    if origin is list:
        inner = get_args(return_type)[0]
        return "list", TypeAdapter(list[inner])

    if origin in (Union, UnionType):
        non_none = [a for a in get_args(return_type) if a is not type(None)]
        if len(non_none) == 1:
            return "single_optional", TypeAdapter(non_none[0])

    if return_type in _SCALAR_TYPES:
        return "scalar", None

    return "single_required", TypeAdapter(return_type)
