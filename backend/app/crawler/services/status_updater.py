from datetime import UTC, datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.crawler.config import CLOSED_DAYS, POSSIBLY_CLOSED_DAYS
from app.models.position import PhdPosition, PositionStatus


async def update_position_statuses(db: AsyncSession) -> dict[str, int]:
    now = datetime.now(UTC)
    today = now.date()
    stats = {"expired": 0, "possibly_closed": 0, "closed": 0}

    expired_result = await db.execute(
        update(PhdPosition)
        .where(
            PhdPosition.deadline.is_not(None),
            PhdPosition.deadline < today,
            PhdPosition.status == PositionStatus.ACTIVE,
        )
        .values(status=PositionStatus.EXPIRED)
    )
    stats["expired"] = expired_result.rowcount or 0

    possibly_cutoff = now - timedelta(days=POSSIBLY_CLOSED_DAYS)
    possibly_result = await db.execute(
        update(PhdPosition)
        .where(
            PhdPosition.last_seen_at.is_not(None),
            PhdPosition.last_seen_at < possibly_cutoff,
            PhdPosition.status == PositionStatus.ACTIVE,
        )
        .values(status=PositionStatus.POSSIBLY_CLOSED)
    )
    stats["possibly_closed"] = possibly_result.rowcount or 0

    closed_cutoff = now - timedelta(days=CLOSED_DAYS)
    closed_result = await db.execute(
        update(PhdPosition)
        .where(
            PhdPosition.last_seen_at.is_not(None),
            PhdPosition.last_seen_at < closed_cutoff,
            PhdPosition.status.in_([PositionStatus.ACTIVE, PositionStatus.POSSIBLY_CLOSED]),
        )
        .values(status=PositionStatus.CLOSED)
    )
    stats["closed"] = closed_result.rowcount or 0

    await db.flush()
    return stats
