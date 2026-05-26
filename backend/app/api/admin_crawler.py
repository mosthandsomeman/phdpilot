from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin
from app.crawler.manager import CrawlerManager
from app.crawler.utils.http_client import HttpClient
from app.database import get_db
from app.models.crawler import CrawlerItem, CrawlerRun
from app.models.user import User
from app.schemas.crawler import CrawlerItemResponse, CrawlerRunRequest, CrawlerRunResponse

router = APIRouter()


@router.post("/run", response_model=list[CrawlerRunResponse])
async def trigger_crawler(
    body: CrawlerRunRequest | None = None,
    _admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    http = HttpClient()
    try:
        manager = CrawlerManager(db, http)
        run_ids = await manager.run_all(sources=body.sources if body else None)
        await db.commit()
        if not run_ids:
            raise HTTPException(status_code=400, detail="No crawler sources executed")
        result = await db.execute(select(CrawlerRun).where(CrawlerRun.id.in_(run_ids)))
        return result.scalars().all()
    finally:
        await http.close()


@router.get("/runs", response_model=list[CrawlerRunResponse])
async def list_runs(
    _admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=20, le=100),
    source_name: str | None = None,
):
    query = select(CrawlerRun).order_by(CrawlerRun.started_at.desc()).limit(limit)
    if source_name:
        query = query.where(CrawlerRun.source_name == source_name)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/runs/{run_id}", response_model=CrawlerRunResponse)
async def get_run(
    run_id: int,
    _admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(CrawlerRun).where(CrawlerRun.id == run_id))
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.get("/items", response_model=list[CrawlerItemResponse])
async def list_items(
    _admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
    run_id: int | None = None,
    status: str | None = None,
    limit: int = Query(default=50, le=200),
):
    query = select(CrawlerItem).order_by(CrawlerItem.created_at.desc()).limit(limit)
    if run_id:
        query = query.where(CrawlerItem.run_id == run_id)
    if status:
        query = query.where(CrawlerItem.status == status)
    result = await db.execute(query)
    return result.scalars().all()
