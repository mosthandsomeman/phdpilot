import logging
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crawler.config import TARGET_KEYWORDS
from app.crawler.utils.country_mapper import all_target_countries
from app.crawler.schemas import CrawlLimits, CrawlStats
from app.crawler.services.database_writer import upsert_position
from app.crawler.services.normalizer import normalize_position
from app.crawler.services.status_updater import update_position_statuses
from app.crawler.sources.academic_positions import AcademicPositionsCrawler
from app.crawler.sources.base import BaseCrawler
from app.crawler.sources.euraxess import EuraxessCrawler
from app.crawler.sources.findaphd import FindAPhDCrawler
from app.crawler.sources.jobs_ac_uk import JobsAcUkCrawler
from app.crawler.utils.country_mapper import resolve_import_country
from app.crawler.utils.http_client import HttpClient
from app.models.crawler import CrawlerItem, CrawlerRun

logger = logging.getLogger(__name__)


def get_crawlers(http: HttpClient) -> list[BaseCrawler]:
    return [
        EuraxessCrawler(http),
        # AcademicPositionsCrawler(http),
        # FindAPhDCrawler(http),
        # JobsAcUkCrawler(http),
    ]


class CrawlerManager:
    def __init__(self, db: AsyncSession, http: HttpClient) -> None:
        self.db = db
        self.http = http

    async def run_all(
        self,
        sources: list[str] | None = None,
        *,
        countries: list[str] | None = None,
        keywords: list[str] | None = None,
        limits: CrawlLimits | None = None,
    ) -> list[int]:
        run_ids: list[int] = []
        country_list = countries or all_target_countries()
        keyword_list = keywords or TARGET_KEYWORDS[:3]

        for crawler in get_crawlers(self.http):
            if sources and crawler.source_name not in sources:
                continue
            run_id = await self.run_source(
                crawler, country_list, keyword_list, limits=limits
            )
            run_ids.append(run_id)

        await update_position_statuses(self.db)
        await self.db.commit()
        return run_ids

    async def run_source(
        self,
        crawler: BaseCrawler,
        countries: list[str],
        keywords: list[str],
        *,
        limits: CrawlLimits | None = None,
    ) -> int:
        run = CrawlerRun(source_name=crawler.source_name, status="running")
        self.db.add(run)
        await self.db.flush()

        stats = CrawlStats()
        try:
            jobs = await crawler.search(countries, keywords, limits=limits)
            stats.fetched = len(jobs)
            logger.info("[%s] Found %s job URLs", crawler.source_name, len(jobs))

            for job in jobs:
                item = CrawlerItem(
                    run_id=run.id,
                    source_name=crawler.source_name,
                    source_url=job.url,
                    status="pending",
                )
                self.db.add(item)
                await self.db.flush()

                try:
                    html = await crawler.fetch_detail(job.url)
                    raw = await crawler.parse_detail(
                        html, job.url, country_hint=job.country_hint
                    )
                    if not raw.get("title"):
                        raise ValueError("Missing title")
                    country, should_skip = resolve_import_country(
                        raw.get("country"), job.country_hint
                    )
                    if should_skip:
                        item.status = "skipped"
                        stats.skipped += 1
                        continue
                    if country:
                        raw["country"] = country

                    normalized = normalize_position(raw, crawler.source_name)
                    result = await upsert_position(self.db, normalized)
                    item.status = result.action
                    if result.action == "created":
                        stats.created += 1
                    elif result.action == "updated":
                        stats.updated += 1
                    else:
                        stats.skipped += 1
                except Exception as e:
                    logger.warning("[%s] Failed %s: %s", crawler.source_name, job.url, e)
                    item.status = "error"
                    item.error_message = str(e)[:500]
                    stats.errors += 1

            run.status = "completed"
        except Exception as e:
            logger.exception("[%s] Run failed: %s", crawler.source_name, e)
            run.status = "failed"
            run.error_message = str(e)[:2000]
        finally:
            run.finished_at = datetime.now(UTC)
            run.total_fetched = stats.fetched
            run.total_created = stats.created
            run.total_updated = stats.updated
            run.total_skipped = stats.skipped
            await self.db.flush()

        return run.id
