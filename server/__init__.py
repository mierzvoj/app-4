from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.routing import Mount

from server.api import api_routes

routes = [
    Mount("/api", routes=api_routes, name="api"),
]


def run():
    middleware = [
        Middleware(TrustedHostMiddleware, allowed_hosts=['*']),
        Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*']),
    ]
    app = Starlette(True, routes, middleware=middleware)

    return app