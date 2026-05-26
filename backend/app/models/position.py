import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.enums import pg_enum


class PositionStatus(str, enum.Enum):
    ACTIVE = "active"
    POSSIBLY_CLOSED = "possibly_closed"
    CLOSED = "closed"
    EXPIRED = "expired"


class PhdPosition(Base):
    __tablename__ = "phd_positions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500))
    university: Mapped[str] = mapped_column(String(300), index=True)
    country: Mapped[str] = mapped_column(String(100), index=True)
    city: Mapped[str | None] = mapped_column(String(100))
    department: Mapped[str | None] = mapped_column(String(300))
    research_area: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    requirements: Mapped[str | None] = mapped_column(Text)
    deadline: Mapped[date | None] = mapped_column(Date)
    salary: Mapped[str | None] = mapped_column(String(100))
    funding: Mapped[str | None] = mapped_column(String(200))
    source_name: Mapped[str | None] = mapped_column(String(100), index=True)
    source_url: Mapped[str | None] = mapped_column(String(1000), unique=True)
    application_url: Mapped[str | None] = mapped_column(String(1000))
    status: Mapped[PositionStatus] = mapped_column(
        pg_enum(PositionStatus), default=PositionStatus.ACTIVE, index=True
    )
    content_hash: Mapped[str | None] = mapped_column(String(64), index=True)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    first_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
