import enum
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.enums import pg_enum


class AiOutputType(str, enum.Enum):
    MATCH = "match"
    PROFESSOR = "professor"
    EMAIL = "email"
    SOP = "sop"
    POLISH = "polish"
    DEEP_RESEARCH = "deep_research"


class AiOutput(Base):
    __tablename__ = "ai_outputs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    position_id: Mapped[int | None] = mapped_column(
        ForeignKey("phd_positions.id", ondelete="SET NULL"), nullable=True
    )
    type: Mapped[AiOutputType] = mapped_column(pg_enum(AiOutputType))
    model_name: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AiUsageLog(Base):
    __tablename__ = "ai_usage_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    model_name: Mapped[str] = mapped_column(String(100))
    input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0)
    credits_cost: Mapped[int] = mapped_column(Integer)
    feature_type: Mapped[str] = mapped_column(String(50))
    latency: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
