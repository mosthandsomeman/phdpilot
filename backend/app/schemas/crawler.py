from datetime import datetime

from pydantic import BaseModel


class CrawlerRunResponse(BaseModel):
    id: int
    source_name: str
    started_at: datetime
    finished_at: datetime | None
    status: str
    total_fetched: int
    total_created: int
    total_updated: int
    total_skipped: int
    error_message: str | None

    model_config = {"from_attributes": True}


class CrawlerItemResponse(BaseModel):
    id: int
    run_id: int
    source_name: str
    source_url: str
    status: str
    error_message: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class CrawlerRunRequest(BaseModel):
    sources: list[str] | None = None
