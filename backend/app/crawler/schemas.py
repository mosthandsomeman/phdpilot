from dataclasses import dataclass
from datetime import date, datetime

from pydantic import BaseModel, Field


@dataclass(frozen=True)
class JobRef:
    url: str
    country_hint: str | None = None


@dataclass(frozen=True)
class CrawlLimits:
    max_jobs: int | None = None
    max_pages: int | None = None


class NormalizedPosition(BaseModel):
    title: str
    university: str | None = None
    country: str | None = None
    city: str | None = None
    department: str | None = None
    research_area: str | None = None
    description: str | None = None
    requirements: str | None = None
    funding: str | None = None
    salary: str | None = None
    deadline: date | None = None
    source_name: str
    source_url: str
    application_url: str | None = None
    status: str = "active"
    content_hash: str = ""


class CrawlStats(BaseModel):
    fetched: int = 0
    created: int = 0
    updated: int = 0
    skipped: int = 0
    errors: int = 0
