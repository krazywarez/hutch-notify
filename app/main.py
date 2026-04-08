from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.db import engine, Base
from app.jobs import start_scheduler, scheduler
from app.routers.health import router as health_router
from app.routers.devices import router as devices_router
from app.routers.subscriptions import router as subscriptions_router
from app.routers.test import router as test_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("select 1"))
    start_scheduler()
    yield
    if scheduler.running:
        scheduler.shutdown(wait=False)
    await engine.dispose()


app = FastAPI(title="hutch-notify", lifespan=lifespan)
app.include_router(health_router)
app.include_router(devices_router)
app.include_router(subscriptions_router)
app.include_router(test_router)
