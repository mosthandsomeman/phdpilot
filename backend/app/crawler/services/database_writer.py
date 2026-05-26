from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crawler.schemas import NormalizedPosition
from app.models.position import PhdPosition, PositionStatus


class UpsertResult:
    def __init__(self, action: str):
        self.action = action  # created | updated | skipped


async def upsert_position(db: AsyncSession, pos: NormalizedPosition) -> UpsertResult:
    now = datetime.now(UTC)
    result = await db.execute(select(PhdPosition).where(PhdPosition.source_url == pos.source_url))
    existing = result.scalar_one_or_none()

    status = PositionStatus.ACTIVE
    if pos.status == "expired":
        status = PositionStatus.EXPIRED
    elif pos.status == "closed":
        status = PositionStatus.CLOSED
    elif pos.status == "possibly_closed":
        status = PositionStatus.POSSIBLY_CLOSED

    if not existing:
        db.add(
            PhdPosition(
                title=pos.title,
                university=pos.university or "Unknown",
                country=pos.country or "Unknown",
                city=pos.city,
                department=pos.department,
                research_area=pos.research_area,
                description=pos.description,
                requirements=pos.requirements,
                funding=pos.funding,
                salary=pos.salary,
                deadline=pos.deadline,
                source_name=pos.source_name,
                source_url=pos.source_url,
                application_url=pos.application_url,
                status=status,
                content_hash=pos.content_hash,
                last_seen_at=now,
                first_seen_at=now,
            )
        )
        await db.flush()
        return UpsertResult("created")

    existing.last_seen_at = now
    if existing.content_hash != pos.content_hash:
        existing.title = pos.title
        existing.university = pos.university or existing.university
        existing.country = pos.country or existing.country
        existing.city = pos.city
        existing.department = pos.department
        existing.research_area = pos.research_area
        existing.description = pos.description
        existing.requirements = pos.requirements
        existing.funding = pos.funding
        existing.salary = pos.salary
        existing.deadline = pos.deadline
        existing.application_url = pos.application_url
        existing.content_hash = pos.content_hash
        existing.status = status
        await db.flush()
        return UpsertResult("updated")

    await db.flush()
    return UpsertResult("skipped")
