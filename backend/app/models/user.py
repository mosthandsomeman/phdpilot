import enum
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import pg_enum


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class MembershipType(str, enum.Enum):
    FREE = "free"
    PRO = "pro"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(pg_enum(UserRole), default=UserRole.USER)
    membership_type: Mapped[MembershipType] = mapped_column(
        pg_enum(MembershipType), default=MembershipType.FREE
    )
    credits: Mapped[int] = mapped_column(Integer, default=100)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    profile: Mapped["UserProfile | None"] = relationship(back_populates="user", uselist=False)
    credit_transactions: Mapped[list["CreditTransaction"]] = relationship(back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    degree: Mapped[str | None] = mapped_column(String(100))
    major: Mapped[str | None] = mapped_column(String(200))
    gpa: Mapped[str | None] = mapped_column(String(20))
    ielts: Mapped[str | None] = mapped_column(String(20))
    research_interests: Mapped[str | None] = mapped_column(Text)
    skills: Mapped[str | None] = mapped_column(Text)
    publications: Mapped[str | None] = mapped_column(Text)
    target_countries: Mapped[str | None] = mapped_column(Text)
    target_fields: Mapped[str | None] = mapped_column(Text)
    cv_url: Mapped[str | None] = mapped_column(String(500))

    user: Mapped["User"] = relationship(back_populates="profile")
