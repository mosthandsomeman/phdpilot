import logging
import re
from urllib.parse import urljoin, urlencode

from bs4 import BeautifulSoup

from app.crawler.config import EURAXESS_COUNTRY_SLUGS, MAX_JOBS_PER_RUN, MAX_PAGES_PER_SOURCE
from app.crawler.parsers.html_cleaner import html_to_text
from app.crawler.schemas import CrawlLimits, JobRef
from app.crawler.sources.base import BaseCrawler
from app.crawler.utils.country_mapper import normalize_country
from app.crawler.utils.date_parser import parse_deadline
from app.crawler.utils.http_client import HttpClient

logger = logging.getLogger(__name__)

BASE_URL = "https://euraxess.ec.europa.eu"
SEARCH_URL = f"{BASE_URL}/jobs/search"


class EuraxessCrawler(BaseCrawler):
    source_name = "EURAXESS"

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def search(
        self,
        countries: list[str],
        keywords: list[str],
        *,
        limits: CrawlLimits | None = None,
    ) -> list[JobRef]:
        jobs: list[JobRef] = []
        seen: set[str] = set()
        keyword = keywords[0] if keywords else "PhD"
        max_jobs = limits.max_jobs if limits and limits.max_jobs else MAX_JOBS_PER_RUN
        max_pages = limits.max_pages if limits and limits.max_pages else MAX_PAGES_PER_SOURCE

        for country in countries:
            slug = EURAXESS_COUNTRY_SLUGS.get(country)
            for page in range(max_pages):
                params: dict[str, str | int] = {
                    "keywords": keyword,
                    "page": page,
                }
                if slug:
                    params["countries"] = slug
                search_url = f"{SEARCH_URL}?{urlencode(params)}"
                try:
                    html = await self.http.get(search_url)
                except Exception as e:
                    logger.warning("EURAXESS search failed %s: %s", search_url, e)
                    break

                page_urls = self._extract_job_links(html)
                if not page_urls:
                    break
                for u in page_urls:
                    if u not in seen:
                        seen.add(u)
                        jobs.append(JobRef(url=u, country_hint=country))
                if len(jobs) >= max_jobs:
                    break
            if len(jobs) >= max_jobs:
                break

        return jobs[:max_jobs]

    def _extract_job_links(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "lxml")
        links: list[str] = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if re.search(r"/jobs/\d+", href):
                full = urljoin(BASE_URL, href.split("?")[0])
                links.append(full)
        return list(dict.fromkeys(links))

    async def fetch_detail(self, url: str) -> str:
        return await self.http.get(url)

    async def parse_detail(
        self, html: str, url: str, *, country_hint: str | None = None
    ) -> dict:
        soup = BeautifulSoup(html, "lxml")
        fields = self._parse_description_list(soup)

        title = self._extract_title(soup)
        university = self._get_field(fields, ["Organisation/Company", "Organisation", "Organization"])
        country_raw = self._get_field(fields, ["Country", "Job country", "Host country"])
        country = normalize_country(country_raw) or country_raw
        city = self._get_field(fields, ["City", "Town"])
        department = self._get_field(fields, ["Department", "Faculty"])
        research_area = self._get_field(
            fields, ["Research Field", "Research field", "Discipline"]
        )
        funding = self._get_field(
            fields,
            [
                "Is the job funded through the EU Research Framework Programme?",
                "Funding",
                "Salary",
            ],
        )
        deadline_text = self._get_field(fields, ["Application Deadline", "Application deadline", "Deadline"])
        deadline = parse_deadline(deadline_text)

        description = html_to_text(html, max_length=4000)
        requirements = self._find_section(soup, ["Requirements", "Qualifications"])

        application_url = None
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True).lower()
            if "apply" in text or "application" in text:
                application_url = urljoin(BASE_URL, a["href"])
                break

        if not country and country_hint:
            country = country_hint

        return {
            "title": title,
            "university": university or "Unknown",
            "country": country,
            "city": city,
            "department": department,
            "research_area": research_area,
            "description": description,
            "requirements": requirements,
            "funding": funding,
            "deadline": deadline,
            "source_url": url,
            "application_url": application_url,
            "status": "active",
        }

    def _parse_description_list(self, soup: BeautifulSoup) -> dict[str, str]:
        data: dict[str, str] = {}
        for dl in soup.select(".ecl-description-list"):
            for dt in dl.find_all("dt", recursive=False):
                label = dt.get_text(strip=True)
                dd = dt.find_next_sibling("dd")
                if label and dd:
                    data[label] = dd.get_text(" ", strip=True)
        return data

    def _get_field(self, fields: dict[str, str], labels: list[str]) -> str | None:
        for label in labels:
            if label in fields:
                return fields[label]
            for key, value in fields.items():
                if key.lower().startswith(label.lower()):
                    return value
        return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        og = soup.find("meta", property="og:title")
        if og and og.get("content"):
            return og["content"].strip()
        h1 = soup.find("h1")
        if h1:
            text = h1.get_text(strip=True)
            if text and text.lower() not in ("job offer", "jobs"):
                return text
        if soup.title:
            return soup.title.get_text(strip=True)
        return "PhD Position"

    def _find_section(self, soup: BeautifulSoup, headings: list[str]) -> str | None:
        for h in soup.find_all(["h2", "h3", "h4", "strong"]):
            if any(hd.lower() in h.get_text(strip=True).lower() for hd in headings):
                parts = []
                for sib in h.find_next_siblings():
                    if sib.name in ("h2", "h3", "h4"):
                        break
                    parts.append(sib.get_text(" ", strip=True))
                if parts:
                    return "\n".join(parts)[:2000]
        return None
