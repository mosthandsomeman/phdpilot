"""Daily crawler task — run once or on schedule.

Usage:
  python -m app.crawler.tasks.daily_update --once
  python -m app.crawler.tasks.daily_update --once --countries Germany --max-jobs 5 --max-pages 1
  python -m app.crawler.tasks.daily_update   # scheduler: daily 03:00 UTC
"""

import argparse
import asyncio
import logging
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database import async_session
from app.crawler.manager import CrawlerManager
from app.crawler.schemas import CrawlLimits
from app.crawler.utils.country_mapper import resolve_countries
from app.crawler.utils.http_client import HttpClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


async def run_daily_crawler(
    sources: list[str] | None = None,
    *,
    countries: list[str] | None = None,
    limits: CrawlLimits | None = None,
) -> list[int]:
    http = HttpClient()
    try:
        async with async_session() as db:
            manager = CrawlerManager(db, http)
            run_ids = await manager.run_all(
                sources=sources, countries=countries, limits=limits
            )
            logger.info("Crawler finished. Run IDs: %s", run_ids)
            return run_ids
    finally:
        await http.close()


async def _scheduler_main(
    sources: list[str] | None,
    countries: list[str] | None,
    limits: CrawlLimits | None,
) -> None:
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(
        run_daily_crawler,
        trigger="cron",
        hour=3,
        minute=0,
        kwargs={"sources": sources, "countries": countries, "limits": limits},
        id="daily_crawler",
    )
    scheduler.start()
    logger.info("Crawler scheduler started (daily at 03:00 UTC)")
    # Run once on startup so data is available immediately
    await run_daily_crawler(sources=sources, countries=countries, limits=limits)
    while True:
        await asyncio.sleep(3600)


def main() -> None:
    parser = argparse.ArgumentParser(description="PhD position daily crawler")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--sources", nargs="*", help="Source names, e.g. EURAXESS")
    parser.add_argument(
        "--countries",
        nargs="+",
        help="Target countries (name or slug), e.g. Germany DE",
    )
    parser.add_argument(
        "--max-jobs",
        type=int,
        help="Max detail pages per run (test runs)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        help="Max search result pages per country (test runs)",
    )
    args = parser.parse_args()

    countries = resolve_countries(args.countries) if args.countries else None
    limits = None
    if args.max_jobs is not None or args.max_pages is not None:
        limits = CrawlLimits(max_jobs=args.max_jobs, max_pages=args.max_pages)

    if args.once:
        asyncio.run(
            run_daily_crawler(sources=args.sources, countries=countries, limits=limits)
        )
        return

    try:
        asyncio.run(_scheduler_main(args.sources, countries, limits))
    except (KeyboardInterrupt, SystemExit):
        logger.info("Crawler scheduler stopped")


if __name__ == "__main__":
    main()
