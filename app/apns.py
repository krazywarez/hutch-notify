from __future__ import annotations

import json
import time
from pathlib import Path

import httpx
import jwt

from app.config import settings


class APNSClient:
    def __init__(self) -> None:
        self._key_text = Path(settings.apns_private_key_path).read_text()
        self._token_cache: tuple[str, int] | None = None
        self._client = httpx.AsyncClient(http2=True, timeout=10.0)

    async def aclose(self) -> None:
        await self._client.aclose()

    def _bearer_token(self) -> str:
        now = int(time.time())
        if self._token_cache and now - self._token_cache[1] < 3000:
            return self._token_cache[0]

        token = jwt.encode(
            {"iss": settings.apns_team_id, "iat": now},
            self._key_text,
            algorithm="ES256",
            headers={"kid": settings.apns_key_id},
        )
        self._token_cache = (token, now)
        return token

    async def send_alert(
        self,
        *,
        device_token: str,
        apns_env: str,
        topic: str,
        title: str,
        body: str,
        payload: dict,
    ) -> tuple[bool, str | None, str | None]:
        host = "https://api.push.apple.com" if apns_env == "production" else "https://api.sandbox.push.apple.com"
        url = f"{host}/3/device/{device_token}"
        merged_payload = {
            "aps": {
                "alert": {"title": title, "body": body},
                "sound": "default",
            },
            **payload,
        }
        response = await self._client.post(
            url,
            headers={
                "authorization": f"bearer {self._bearer_token()}",
                "apns-topic": topic,
                "apns-push-type": "alert",
                "apns-priority": "10",
            },
            content=json.dumps(merged_payload).encode("utf-8"),
        )
        apns_id = response.headers.get("apns-id")
        if 200 <= response.status_code < 300:
            return True, apns_id, None
        error = None
        try:
            error = response.json().get("reason")
        except Exception:
            error = response.text
        return False, apns_id, error
