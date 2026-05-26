import asyncio
import logging
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx

from app.crawler.config import (
    CRAWLER_FROM_HEADER,
    CRAWLER_USER_AGENT,
    MAX_RETRIES,
    REQUEST_DELAY_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
)

logger = logging.getLogger(__name__)

_domain_last_request: dict[str, float] = {}
_robots_cache: dict[str, RobotFileParser] = {}
_warmed_domains: set[str] = set()

BROWSER_HEADERS = {
    "User-Agent": CRAWLER_USER_AGENT,
    "From": CRAWLER_FROM_HEADER,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}


class HttpClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            headers=BROWSER_HEADERS,
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def _rate_limit(self, url: str) -> None:
        domain = urlparse(url).netloc
        now = asyncio.get_event_loop().time()
        last = _domain_last_request.get(domain, 0.0)
        wait = REQUEST_DELAY_SECONDS - (now - last)
        if wait > 0:
            await asyncio.sleep(wait)
        _domain_last_request[domain] = asyncio.get_event_loop().time()

    async def _warmup_domain(self, url: str) -> None:
        """Visit site root once per domain to obtain cookies (reduces 403 from WAF)."""
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        if base in _warmed_domains:
            return
        try:
            await self._rate_limit(base)
            resp = await self._client.get(base, headers={**BROWSER_HEADERS, "Referer": base})
            if resp.status_code < 400:
                _warmed_domains.add(base)
                logger.info("Warmed up session for %s", base)
        except Exception as e:
            logger.warning("Domain warmup failed for %s: %s", base, e)

    async def _can_fetch(self, url: str) -> bool:
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        if base not in _robots_cache:
            rp = RobotFileParser()
            robots_url = f"{base}/robots.txt"
            try:
                resp = await self._client.get(robots_url)
                if resp.status_code == 200:
                    rp.parse(resp.text.splitlines())
                else:
                    rp.allow_all = True
            except Exception:
                rp.allow_all = True
            _robots_cache[base] = rp
        return _robots_cache[base].can_fetch("*", url)

    def _request_headers(self, url: str) -> dict[str, str]:
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        headers = dict(BROWSER_HEADERS)
        headers["Referer"] = base if "/jobs/" not in url else f"{base}/jobs"
        if "/jobs/search" in url:
            headers["Sec-Fetch-Site"] = "same-origin"
        return headers

    async def get(self, url: str) -> str:
        if not await self._can_fetch(url):
            raise PermissionError(f"robots.txt disallows: {url}")

        await self._warmup_domain(url)

        last_error: Exception | None = None
        for attempt in range(MAX_RETRIES):
            await self._rate_limit(url)
            try:
                resp = await self._client.get(url, headers=self._request_headers(url))
                if resp.status_code == 403:
                    raise httpx.HTTPStatusError(
                        "403 Forbidden — site may block datacenter IPs",
                        request=resp.request,
                        response=resp,
                    )
                resp.raise_for_status()
                return resp.text
            except Exception as e:
                last_error = e
                logger.warning("HTTP GET failed %s (attempt %s): %s", url, attempt + 1, e)
                await asyncio.sleep(2**attempt)
        raise RuntimeError(f"Failed to fetch {url}") from last_error
