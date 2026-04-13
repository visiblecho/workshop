import uuid
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import String, Integer, ForeignKey, Text, Numeric, Date, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from .base import Base, Segment, Unit


class JobType(Base):
    __tablename__ = "job_type"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    segment: Mapped[Segment] = mapped_column(SAEnum(Segment, name="segment", create_constraint=False, native_enum=False), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("job_type.id"), nullable=True)
    avg_duration_h: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    avg_margin_pct: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    sample_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)


class Article(Base):
    __tablename__ = "article"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    segment: Mapped[Segment] = mapped_column(SAEnum(Segment, name="segment", create_constraint=False, native_enum=False), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    datanorm_id: Mapped[str | None] = mapped_column(String, nullable=True)
    unit: Mapped[Unit] = mapped_column(SAEnum(Unit, name="unit", create_constraint=False, native_enum=False), nullable=False)
    default_price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    wholesaler: Mapped[str | None] = mapped_column(String, nullable=True)
    last_price_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
