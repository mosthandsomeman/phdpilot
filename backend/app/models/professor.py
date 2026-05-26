from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Professor(Base):
    __tablename__ = "professors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200))
    university: Mapped[str] = mapped_column(String(300), index=True)
    department: Mapped[str | None] = mapped_column(String(300))
    email: Mapped[str | None] = mapped_column(String(255))
    homepage_url: Mapped[str | None] = mapped_column(String(1000))
    research_interests: Mapped[str | None] = mapped_column(Text)
    recent_papers: Mapped[str | None] = mapped_column(Text)
