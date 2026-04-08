# hutch-notify

Minimal backend for push notifications in Hutch.

## Purpose

- register APNs device tokens
- store notification subscriptions
- poll sr.ht for changes
- send push notifications via APNs

Designed to be:
- simple
- cheap to run
- easy to reason about

## Stack

- Python (FastAPI)
- SQLite (initially)
- APNs (HTTP/2, token-based auth)

## Status

Early development.

Current scope:
- device registration
- test push endpoint

Planned:
- build notifications
- ticket notifications
- inbox notifications (later)

## Running locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or use pyproject

uvicorn app.main:app --reload
```

## Environment

Create an `.env` file:

```bash
API_KEY=change-me
DATABASE_URL=sqlite+aiosqlite:///./hutch_notify.db

APNS_KEY_ID=
APNS_TEAM_ID=
APNS_BUNDLE_ID=
APNS_PRIVATE_KEY_PATH=

SRHT_TOKEN=
```

## Notes

- iOS app must register with APNs and send device token to this server
- APNs key (`.p8`) must be kept secure
- Notifications are event-driven, but initial version uses polling

