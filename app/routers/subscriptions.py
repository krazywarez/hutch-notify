from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas import SubscriptionUpsertIn
from app.crud import replace_subscriptions
from app.security import require_api_key

router = APIRouter(prefix="/v1/subscriptions", tags=["subscriptions"], dependencies=[Depends(require_api_key)])


@router.post("/upsert")
async def upsert_subscriptions(payload: SubscriptionUpsertIn, db: AsyncSession = Depends(get_db)) -> dict:
    await replace_subscriptions(db, payload)
    return {"status": "ok"}
