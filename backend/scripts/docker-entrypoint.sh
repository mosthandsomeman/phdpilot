#!/bin/sh
set -e

echo "[entrypoint] Running alembic upgrade head..."
if alembic upgrade head; then
  echo "[entrypoint] Migrations OK."
else
  echo "[entrypoint] Migration failed — checking for existing schema..."
  python - <<'PY'
import asyncio
import subprocess
import sys

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import get_settings


async def main() -> None:
    engine = create_async_engine(get_settings().database_url)
    async with engine.connect() as conn:
        users = (
            await conn.execute(
                text(
                    "SELECT EXISTS ("
                    "  SELECT 1 FROM information_schema.tables "
                    "  WHERE table_schema = 'public' AND table_name = 'users'"
                    ")"
                )
            )
        ).scalar()
    await engine.dispose()
    if not users:
        print("[entrypoint] No users table — migration must succeed.", file=sys.stderr)
        sys.exit(1)
    print("[entrypoint] Schema exists — stamping alembic head.")
    subprocess.run(["alembic", "stamp", "head"], check=True)


asyncio.run(main())
PY
fi

echo "[entrypoint] Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
