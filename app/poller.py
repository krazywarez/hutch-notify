from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Subscription, Event, Delivery, Device


async def poll_builds_once(db: AsyncSession) -> None:
    # Placeholder.
    # Replace with sr.ht fetch logic.
    # Strategy:
    # 1. query distinct build subscriptions
    # 2. fetch latest builds per source_id
    # 3. create Event rows for unseen terminal states
    # 4. create Delivery rows for enabled devices subscribed to matching event_type
    subscribed = await db.execute(
        select(Subscription).where(Subscription.source_type == "build", Subscription.is_enabled.is_(True))
    )
    subscriptions = subscribed.scalars().all()

    # no-op until sr.ht integration is wired
    _ = subscriptions
