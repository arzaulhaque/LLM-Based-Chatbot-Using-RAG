from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.exceptions import add_exception_handlers
from app.core.logging import configure_logging
from app.infrastructure.db.models import user as _user_model  # noqa: F401
from app.infrastructure.db.session import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


def create_application() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title=settings.APP_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    add_exception_handlers(app)
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/health", tags=["health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_application()
