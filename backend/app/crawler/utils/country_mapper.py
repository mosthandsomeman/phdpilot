from app.crawler.config import EURAXESS_COUNTRY_SLUGS, TARGET_COUNTRIES

_ALL = [c for group in TARGET_COUNTRIES.values() for c in group]

_ALIASES: dict[str, str] = {
    "deutschland": "Germany",
    "germany": "Germany",
    "nederland": "Netherlands",
    "netherlands": "Netherlands",
    "sverige": "Sweden",
    "sweden": "Sweden",
    "norge": "Norway",
    "norway": "Norway",
    "danmark": "Denmark",
    "denmark": "Denmark",
    "suomi": "Finland",
    "finland": "Finland",
    "ísland": "Iceland",
    "iceland": "Iceland",
    "italia": "Italy",
    "italy": "Italy",
    "españa": "Spain",
    "spain": "Spain",
    "portugal": "Portugal",
    "ελλάδα": "Greece",
    "greece": "Greece",
}


def normalize_country(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = value.strip()
    for target in _ALL:
        if target.lower() in cleaned.lower():
            return target
    key = cleaned.lower()
    return _ALIASES.get(key, cleaned if cleaned in _ALL else None)


def is_target_country(country: str | None) -> bool:
    if not country:
        return False
    normalized = normalize_country(country)
    return normalized in _ALL if normalized else False


def resolve_import_country(
    parsed: str | None,
    hint: str | None,
) -> tuple[str | None, bool]:
    """Return (country to store, should_skip).

    Trust search country_hint when the listing was fetched in a target-country search.
    Skip only when the page clearly names a non-target country and there is no target hint.
    """
    parsed_n = normalize_country(parsed)
    hint_n = normalize_country(hint)

    if hint_n and is_target_country(hint_n):
        if parsed_n and is_target_country(parsed_n):
            return parsed_n, False
        return hint_n, False

    if parsed_n:
        if is_target_country(parsed_n):
            return parsed_n, False
        return parsed_n, True

    if hint_n:
        return hint_n, False

    return None, False


def all_target_countries() -> list[str]:
    return list(_ALL)


_SLUG_TO_COUNTRY = {slug.upper(): name for name, slug in EURAXESS_COUNTRY_SLUGS.items()}


def resolve_countries(names: list[str]) -> list[str]:
    """Resolve country names or EURAXESS slugs (e.g. Germany, DE) to canonical names."""
    by_name = {c.lower(): c for c in _ALL}
    resolved: list[str] = []
    for raw in names:
        token = raw.strip()
        if not token:
            continue
        if token.lower() in by_name:
            resolved.append(by_name[token.lower()])
        elif token.upper() in _SLUG_TO_COUNTRY:
            resolved.append(_SLUG_TO_COUNTRY[token.upper()])
        else:
            options = ", ".join(_ALL)
            raise ValueError(f"Unknown country '{raw}'. Valid: {options} (or slugs DE, SE, …)")
    if not resolved:
        raise ValueError("At least one country is required")
    return resolved
