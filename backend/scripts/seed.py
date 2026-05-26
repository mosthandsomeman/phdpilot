"""Seed sample PhD positions for development.

Run inside Docker:
  docker compose exec backend python scripts/seed.py
"""

import asyncio
import sys
from datetime import date, timedelta
from pathlib import Path

# Allow `python scripts/seed.py` when cwd is /app
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select

from app.database import async_session
from app.models.position import PhdPosition, PositionStatus


SAMPLE_POSITIONS = [
    {
        "title": "PhD in Machine Learning for Healthcare",
        "university": "ETH Zurich",
        "country": "Switzerland",
        "city": "Zurich",
        "department": "Computer Science",
        "research_area": "Medical AI, Deep Learning",
        "description": "Develop novel ML methods for clinical decision support.",
        "funding": "Fully funded",
        "deadline": date.today() + timedelta(days=60),
        "source_name": "EURAXESS",
    },
    {
        "title": "Doctoral Researcher in Agricultural Robotics",
        "university": "Wageningen University",
        "country": "Netherlands",
        "city": "Wageningen",
        "department": "Agrotechnology",
        "research_area": "Robotics, Computer Vision",
        "description": "Research autonomous systems for precision agriculture.",
        "funding": "4-year contract",
        "deadline": date.today() + timedelta(days=45),
        "source_name": "FindAPhD",
    },
    {
        "title": "PhD Position in Trustworthy AI",
        "university": "Technical University of Munich",
        "country": "Germany",
        "city": "Munich",
        "department": "Informatics",
        "research_area": "AI Safety, Explainability",
        "description": "Build interpretable and robust AI systems.",
        "funding": "TV-L E13",
        "deadline": date.today() + timedelta(days=30),
        "source_name": "Academic Positions",
    },
]


async def seed():
    async with async_session() as db:
        existing = await db.execute(select(PhdPosition).limit(1))
        if existing.scalar_one_or_none():
            print("Positions already seeded, skipping.")
            return

        for data in SAMPLE_POSITIONS:
            db.add(PhdPosition(status=PositionStatus.ACTIVE, **data))
        await db.commit()
        print(f"Seeded {len(SAMPLE_POSITIONS)} positions.")


if __name__ == "__main__":
    asyncio.run(seed())
