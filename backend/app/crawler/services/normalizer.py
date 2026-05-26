from app.crawler.schemas import NormalizedPosition
from app.crawler.utils.country_mapper import normalize_country
from app.crawler.utils.hash import build_content_hash


def normalize_position(raw: dict, source_name: str) -> NormalizedPosition:
    country = normalize_country(raw.get("country"))
    data = {
        "title": (raw.get("title") or "Untitled position").strip()[:500],
        "university": (raw.get("university") or "Unknown")[:300],
        "country": country or raw.get("country") or "Unknown",
        "city": raw.get("city"),
        "department": raw.get("department"),
        "research_area": raw.get("research_area"),
        "description": raw.get("description"),
        "requirements": raw.get("requirements"),
        "funding": raw.get("funding"),
        "salary": raw.get("salary"),
        "deadline": raw.get("deadline"),
        "source_name": source_name,
        "source_url": raw["source_url"],
        "application_url": raw.get("application_url"),
        "status": raw.get("status") or "active",
    }
    content_hash = build_content_hash(data)
    return NormalizedPosition(**data, content_hash=content_hash)
