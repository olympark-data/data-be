from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """모든 SQLAlchemy 모델의 부모 (Spring의 @Entity 기준 클래스)."""


class TimestampMixin:
    """공통 컬럼 (Spring BaseEntity의 createdAt, updatedAt)."""

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
