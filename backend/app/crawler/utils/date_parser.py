import re
from datetime import date, datetime

_DATE_PATTERNS = [
    ("%Y-%m-%d", r"\d{4}-\d{2}-\d{2}"),
    ("%d/%m/%Y", r"\d{1,2}/\d{1,2}/\d{4}"),
    ("%d %B %Y", None),
    ("%B %d, %Y", None),
]


def parse_deadline(text: str | None) -> date | None:
    if not text:
        return None
    text = text.strip()
    iso = re.search(r"(\d{4}-\d{2}-\d{2})", text)
    if iso:
        try:
            return datetime.strptime(iso.group(1), "%Y-%m-%d").date()
        except ValueError:
            pass
    for fmt, _ in _DATE_PATTERNS:
        if fmt is None:
            continue
        try:
            m = re.search(r"(\d{1,2}[/.-]\d{1,2}[/.-]\d{4})", text)
            if m:
                sep = "/" if "/" in m.group(1) else "-"
                parts = re.split(r"[/.-]", m.group(1))
                if len(parts) == 3:
                    d, mo, y = int(parts[0]), int(parts[1]), int(parts[2])
                    return date(y, mo, d)
        except (ValueError, IndexError):
            continue
    return None
