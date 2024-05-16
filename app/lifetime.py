from typing import Callable, Awaitable

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.app import settings


def _setup_db(app: FastAPI) -> None:
    engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)

    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


def register_startup_event(
        app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        app.middleware_stack = None
        _setup_db(app)
        app.middleware_stack = app.build_middleware_stack()
        pass  # noqa: WPS420

    return _startup


def register_shutdown_event(
        app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        await app.state.db_engine.dispose()

        pass  # noqa: WPS420

    return _shutdown
