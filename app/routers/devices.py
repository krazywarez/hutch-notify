from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas import DeviceRegisterIn
from app.crud import upsert_device
from app.security import require_api_key

router = APIRouter(prefix="/v1/devices", tags=["devices"], dependencies=[Depends(require_api_key)])


@router.post("/register")
async def register_device(payload: DeviceRegisterIn, db: AsyncSession = Depends(get_db)) -> dict:
    device = await upsert_device(db, payload)
    return {
        "id": device.id,
        "user_id": device.user_id,
        "bundle_id": device.bundle_id,
        "apns_env": device.apns_env,
        "is_enabled": device.is_enabled,
    }
