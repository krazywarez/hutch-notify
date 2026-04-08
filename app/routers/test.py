from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.apns import APNSClient
from app.db import get_db
from app.models import Device
from app.security import require_api_key

router = APIRouter(prefix="/v1/test", tags=["test"], dependencies=[Depends(require_api_key)])


@router.post("/push/{device_id}")
async def test_push(device_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if device is None:
        raise HTTPException(status_code=404, detail="device not found")

    client = APNSClient()
    try:
        ok, apns_id, error = await client.send_alert(
            device_token=device.apns_token,
            apns_env=device.apns_env,
            topic=device.bundle_id,
            title="Hutch test",
            body="Test push from hutch-notify",
            payload={"event_type": "test", "deep_link": "hutch://home"},
        )
    finally:
        await client.aclose()

    return {"ok": ok, "apns_id": apns_id, "error": error}
