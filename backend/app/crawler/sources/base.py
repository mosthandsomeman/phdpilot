from abc import ABC, abstractmethod

from app.crawler.schemas import CrawlLimits, JobRef


class BaseCrawler(ABC):
    source_name: str

    @abstractmethod
    async def search(
        self,
        countries: list[str],
        keywords: list[str],
        *,
        limits: CrawlLimits | None = None,
    ) -> list[JobRef]:
        """Return job detail references (URL + optional country from search context)."""

    @abstractmethod
    async def fetch_detail(self, url: str) -> str:
        """Fetch detail page HTML."""

    @abstractmethod
    async def parse_detail(
        self, html: str, url: str, *, country_hint: str | None = None
    ) -> dict:
        """Parse detail page into raw field dict (must include source_url)."""
