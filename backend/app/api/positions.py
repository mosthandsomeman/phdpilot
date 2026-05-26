from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_optional_user
from app.database import get_db
from app.models.position import PhdPosition, PositionStatus
from app.models.user import User
from app.schemas.position import PositionListResponse, PositionResponse

router = APIRouter()

OPEN_STATUSES = [PositionStatus.ACTIVE, PositionStatus.POSSIBLY_CLOSED]


@router.get("", response_model=PositionListResponse)
async def list_positions(
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    country: str | None = None,
    research_area: str | None = None,
    funding: str | None = None,
    source_name: str | None = None,
    status: str | None = Query(default="active"),
    deadline_before: date | None = None,
    deadline_after: date | None = None,
    sort: str = Query(default="deadline", pattern="^(deadline|created_at|title)$"),
    q: str | None = None,
    _user: User | None = Depends(get_optional_user),
):
    query = select(PhdPosition)
    count_query = select(func.count()).select_from(PhdPosition)

    if status == "active":
        query = query.where(PhdPosition.status.in_(OPEN_STATUSES))
        count_query = count_query.where(PhdPosition.status.in_(OPEN_STATUSES))
    elif status and status != "all":
        try:
            status_enum = PositionStatus(status)
            query = query.where(PhdPosition.status == status_enum)
            count_query = count_query.where(PhdPosition.status == status_enum)
        except ValueError:
            pass

    if country:
        query = query.where(PhdPosition.country.ilike(f"%{country}%"))
        count_query = count_query.where(PhdPosition.country.ilike(f"%{country}%"))
    if research_area:
        pattern = f"%{research_area}%"
        query = query.where(PhdPosition.research_area.ilike(pattern))
        count_query = count_query.where(PhdPosition.research_area.ilike(pattern))
    if funding:
        query = query.where(PhdPosition.funding.ilike(f"%{funding}%"))
        count_query = count_query.where(PhdPosition.funding.ilike(f"%{funding}%"))
    if source_name:
        query = query.where(PhdPosition.source_name.ilike(f"%{source_name}%"))
        count_query = count_query.where(PhdPosition.source_name.ilike(f"%{source_name}%"))
    if deadline_before:
        query = query.where(PhdPosition.deadline <= deadline_before)
        count_query = count_query.where(PhdPosition.deadline <= deadline_before)
    if deadline_after:
        query = query.where(PhdPosition.deadline >= deadline_after)
        count_query = count_query.where(PhdPosition.deadline >= deadline_after)
    if q:
        pattern = f"%{q}%"
        text_filter = (
            PhdPosition.title.ilike(pattern)
            | PhdPosition.university.ilike(pattern)
            | PhdPosition.research_area.ilike(pattern)
            | PhdPosition.description.ilike(pattern)
        )
        query = query.where(text_filter)
        count_query = count_query.where(text_filter)

    total = (await db.execute(count_query)).scalar() or 0
    offset = (page - 1) * page_size

    if sort == "title":
        order = PhdPosition.title.asc()
    elif sort == "created_at":
        order = PhdPosition.created_at.desc()
    else:
        order = PhdPosition.deadline.asc().nullslast()

    result = await db.execute(query.order_by(order, PhdPosition.created_at.desc()).offset(offset).limit(page_size))
    items = result.scalars().all()
    return PositionListResponse(
        items=[PositionResponse.model_validate(p) for p in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{position_id}", response_model=PositionResponse)
async def get_position(position_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PhdPosition).where(PhdPosition.id == position_id))
    position = result.scalar_one_or_none()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position
