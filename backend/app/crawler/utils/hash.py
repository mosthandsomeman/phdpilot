import hashlib


def build_content_hash(position: dict) -> str:
    raw = "|".join(
        [
            position.get("title") or "",
            position.get("university") or "",
            position.get("country") or "",
            position.get("description") or "",
            position.get("requirements") or "",
            str(position.get("deadline") or ""),
        ]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
