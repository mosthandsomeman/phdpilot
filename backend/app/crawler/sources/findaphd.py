from app.crawler.schemas import CrawlLimits, JobRef
from app.crawler.sources.base import BaseCrawler
from app.crawler.utils.http_client import HttpClient


class FindAPhDCrawler(BaseCrawler):
    """Placeholder — Phase 2."""

    source_name = "FindAPhD"

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def search(
        self,
        countries: list[str],
        keywords: list[str],
        *,
        limits: CrawlLimits | None = None,
    ) -> list[JobRef]:
        return []

    async def fetch_detail(self, url: str) -> str:
        return ""

    async def parse_detail(
        self, html: str, url: str, *, country_hint: str | None = None
    ) -> dict:
        return {"source_url": url, "title": ""}
