"""Quick EURAXESS crawl for a single country (small limits for testing).

Run inside Docker:
  docker compose exec crawler python scripts/crawl_one_country.py
  docker compose exec crawler python scripts/crawl_one_country.py --country Sweden --max-jobs 3
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.crawler.schemas import CrawlLimits
from app.crawler.tasks.daily_update import run_daily_crawler
from app.crawler.utils.country_mapper import resolve_countries

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="EURAXESS single-country test crawl")
    parser.add_argument(
        "--country",
        default="Germany",
        help="Country name or slug (default: Germany)",
    )
    parser.add_argument(
        "--max-jobs",
        type=int,
        default=5,
        help="Max job detail pages to fetch (default: 5)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=1,
        help="Max search pages for this country (default: 1)",
    )
    args = parser.parse_args()

    countries = resolve_countries([args.country])
    limits = CrawlLimits(max_jobs=args.max_jobs, max_pages=args.max_pages)

    logger.info(
        "Test crawl: source=EURAXESS country=%s max_jobs=%s max_pages=%s",
        countries[0],
        args.max_jobs,
        args.max_pages,
    )
    run_ids = asyncio.run(
        run_daily_crawler(
            sources=["EURAXESS"],
            countries=countries,
            limits=limits,
        )
    )
    logger.info("Done. Run IDs: %s", run_ids)


if __name__ == "__main__":
    main()
