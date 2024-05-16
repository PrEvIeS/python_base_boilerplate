from importlib import metadata
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.staticfiles import StaticFiles

from app.lifetime import register_startup_event, register_shutdown_event
from app.routes.router import api_router
from config.logging import setup_logging

APP_ROOT = Path(__file__).parent


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="base",
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    register_startup_event(app)
    register_shutdown_event(app)

    app.include_router(router=api_router, prefix="/api")

    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT.parent / "static"),
        name="static",
    )

    return app
