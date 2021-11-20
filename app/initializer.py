from inspect import getmembers
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import settings
from app.schema.internal import TypedAPIRouter


def init(app: FastAPI):
    """
    Main Init
    :param app:
    :return:
    """
    cfg = settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    init_sentry(app, cfg)
    init_routers(app)


def init_sentry(app: FastAPI, cfg):
    if cfg.sentry_dsn:
        import sentry_sdk
        from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
        sentry_sdk.init(dsn=cfg.sentry_dsn, environment=cfg.app_env, send_default_pii=True)
        app.add_middleware(SentryAsgiMiddleware)


def init_routers(app: FastAPI):
    from app import routes

    routers = [o[1] for o in getmembers(routes) if isinstance(o[1], TypedAPIRouter)]

    for router in routers:
        app.include_router(**router.dict())
