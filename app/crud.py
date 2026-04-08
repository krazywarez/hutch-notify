from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Device, Subscription, Event, Delivery
from app.schemas import DeviceRegisterIn, SubscriptionUpsertIn


async def upsert_device(db: AsyncSession, payload: DeviceRegisterIn) -> Device:
    stmt = select(Device).where(
        Device.apns_token == payload.apns_token,
        Device.bundle_id == payload.bundle_id,
    )
    result = await db.execute(stmt)
    device = result.scalar_one_or_none()

    if device is None:
        device = Device(
            user_id=payload.user_id,
            apns_token=payload.apns_token,
            apns_env=payload.apns_env,
            bundle_id=payload.bundle_id,
            platform=payload.platform,
            app_version=payload.app_version,
            device_name=payload.device_name,
            is_enabled=True,
            last_seen_at=datetime.utcnow(),
        )
        db.add(device)
    else:
        device.user_id = payload.user_id
        device.apns_env = payload.apns_env
        device.platform = payload.platform
        device.app_version = payload.app_version
        device.device_name = payload.device_name
        device.is_enabled = True
        device.last_seen_at = datetime.utcnow()

    await db.commit()
    await db.refresh(device)
    return device


async def replace_subscriptions(db: AsyncSession, payload: SubscriptionUpsertIn) -> None:
    await db.execute(delete(Subscription).where(Subscription.device_id == payload.device_id))
    for item in payload.subscriptions:
        db.add(
            Subscription(
                device_id=payload.device_id,
                source_type=item.source_type,
                source_id=item.source_id,
                event_type=item.event_type,
                is_enabled=item.is_enabled,
            )
        )
    await db.commit()
