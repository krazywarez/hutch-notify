from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config import settings
from app.db import SessionLocal
from app.poller import poll_builds_once

scheduler = AsyncIOScheduler()


def start_scheduler() -> None:
    scheduler.add_job(run_build_poll, "interval", seconds=settings.poll_interval_seconds, id="build-poll", replace_existing=True)
    scheduler.start()


async def run_build_poll() -> None:
    async with SessionLocal() as db:
        await poll_builds_once(db)
