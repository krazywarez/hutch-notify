from pydantic import BaseModel, Field


class DeviceRegisterIn(BaseModel):
    user_id: str
    apns_token: str = Field(min_length=16)
    apns_env: str
    bundle_id: str
    platform: str = "ios"
    app_version: str | None = None
    device_name: str | None = None


class DeviceOut(BaseModel):
    id: int
    user_id: str
    bundle_id: str
    apns_env: str
    is_enabled: bool


class SubscriptionIn(BaseModel):
    source_type: str
    source_id: str
    event_type: str
    is_enabled: bool = True


class SubscriptionUpsertIn(BaseModel):
    device_id: int
    subscriptions: list[SubscriptionIn]
