#!/bin/sh
set -e

run_migrate() {
  alembic upgrade head
}

cleanup_orphan_enums() {
  python - <<'PY'
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import get_settings

ENUM_TYPES = (
    "userrole",
    "membershiptype",
    "positionstatus",
    "credittransactiontype",
    "applicationstatus",
    "aioutputtype",
)

async def main() -> None:
    engine = create_async_engine(get_settings().database_url)
    async with engine.begin() as conn:
        for name in ENUM_TYPES:
            await conn.execute(text(f'DROP TYPE IF EXISTS "{name}" CASCADE'))
    await engine.dispose()

asyncio.run(main())
PY
}

echo "[entrypoint] Running alembic upgrade head..."
if run_migrate; then
  echo "[entrypoint] Migrations OK."
else
  echo "[entrypoint] Migration failed — dropping orphan enum types and retrying..."
  cleanup_orphan_enums
  if ! run_migrate; then
    echo "[entrypoint] Still failing. Reset database:" >&2
    echo "  docker compose exec postgres psql -U phdpilot -d phdpilot -c \"DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO phdpilot; GRANT ALL ON SCHEMA public TO public; CREATE EXTENSION IF NOT EXISTS vector;\"" >&2
    exit 1
  fi
  echo "[entrypoint] Migrations OK after enum cleanup."
fi

echo "[entrypoint] Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
