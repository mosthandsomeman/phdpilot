from datetime import date, datetime

from pydantic import BaseModel


class PositionResponse(BaseModel):
    id: int
    title: str
    university: str
    country: str
    city: str | None
    department: str | None
    research_area: str | None
    description: str | None
    requirements: str | None
    deadline: date | None
    salary: str | None
    funding: str | None
    source_name: str | None
    source_url: str | None
    application_url: str | None = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class PositionListResponse(BaseModel):
    items: list[PositionResponse]
    total: int
    page: int
    page_size: int
