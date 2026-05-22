from functools import wraps
from typing import Any, Callable

from sqlalchemy.ext.asyncio import AsyncSession


def _resolve_session(obj: Any, path: str) -> AsyncSession:
    for part in path.split("."):
        obj = getattr(obj, part)
    return obj


def transactional(func: Callable | None = None, *, read_only: bool = False):
    def decorator(f: Callable):
        @wraps(f)
        async def wrapper(self, *args, **kwargs):
            path: str | None = getattr(type(self), "__session_attr__", None)
            if path is None:
                raise AttributeError(
                    f"{type(self).__name__} debe declarar "
                    f"`__session_attr__` para usar @transactional "
                    f"(p. ej. `__session_attr__ = 'plan_repository.session'`)."
                )
            session: AsyncSession = _resolve_session(self, path)

            if read_only:
                return await f(self, *args, **kwargs)

            async with session.begin():
                return await f(self, *args, **kwargs)

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator
