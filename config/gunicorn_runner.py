from typing import Any

from gunicorn.app.base import BaseApplication
from gunicorn.util import import_app
from uvicorn.workers import UvicornWorker

try:
    import uvloop
except ImportError:
    uvloop = None


class Worker(UvicornWorker):
    CONFIG_KWARGS = {
        "loop": "uvloop" if uvloop is not None else "asyncio",
        "http": "httptools",
        "lifespan": "on",
        "factory": True,
        "proxy_headers": False,
    }


class GunicornApplication(BaseApplication):
    def __init__(
            self,
            app: str,
            host: str,
            port: int,
            workers: int,
            **kwargs: Any
    ):
        self.options = {
            "bind": f"{host}:{port}",
            "workers": workers,
            "worker_class": "config.gunicorn_runner.UvicornWorker",
            **kwargs,
        }
        self.app = app
        super().__init__()

    def load_config(self) -> None:
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self) -> str:
        """
        Load actual application.

        Gunicorn loads application based on this
        function's returns. We return python's path to
        the app's factory.

        :returns: python path to app factory.
        """
        return import_app(self.app)
