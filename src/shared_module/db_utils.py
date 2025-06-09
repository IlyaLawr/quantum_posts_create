from typing import Callable, TypeVar
from functools import wraps

from sqlalchemy.ext.asyncio import create_async_engine

from shared_module.models import Base
from shared_module.settings import settings

engine = create_async_engine(settings.db_url, echo=settings.db_logs)

T = TypeVar('T')


def decorate_all_methods(decorator):
    def decorate(cls):
        for name, value in cls.__dict__.items():
            if callable(value) and not name.startswith("__"):
                setattr(cls, name, decorator(value))
        return cls
    return decorate


def connect(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    async def wrapper(self, *args, **kwargs) -> T:
        async with engine.connect() as connect:
            return await func(self, connect, *args, **kwargs)
    return wrapper


def create_table() -> None:

    async def create() -> None:
        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    from asyncio import get_running_loop, run

    try:
        loop = get_running_loop()
        loop.create_task(create())
    except RuntimeError:
        run(create())
