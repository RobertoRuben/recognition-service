from functools import wraps
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession


def transactional(func: Callable | None = None, *, read_only: bool = False):
    def decorator(f: Callable):
        @wraps(f)
        async def wrapper(self, *args, **kwargs):
            session: AsyncSession = self.session

            if read_only:
                return await f(self, *args, **kwargs)

            async with session.begin():
                return await f(self, *args, **kwargs)

        return wrapper

    if func is not None:
        return decorator(func)

    return decorator
