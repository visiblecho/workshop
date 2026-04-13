import uuid
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import String, Integer, ForeignKey, Numeric, Date, Index, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from .base import Base, Segment, CLMetric


class CLBenchmark(Base):
    __tablename__ = "cl_benchmark"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("job_type.id"), nullable=False)
    segment: Mapped[Segment] = mapped_column(SAEnum(Segment, name="segment", create_constraint=False, native_enum=False), nullable=False)
    region: Mapped[str] = mapped_column(String, nullable=False)
    metric: Mapped[CLMetric] = mapped_column(SAEnum(CLMetric, name="cl_metric", create_constraint=False, native_enum=False), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False)
    p25: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    p50: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    p75: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    mean: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_cl_benchmark_lookup", "job_type_id", "segment", "region", "metric", "currency"),
    )


class FirmBenchmark(Base):
    __tablename__ = "firm_benchmark"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("firm.id"), nullable=False)
    job_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("job_type.id"), nullable=False)
    metric: Mapped[CLMetric] = mapped_column(SAEnum(CLMetric, name="cl_metric", create_constraint=False, native_enum=False), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False)
    p25: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    p50: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    p75: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    mean: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_firm_benchmark_lookup", "firm_id", "job_type_id", "metric"),
    )


class ArticlePriceHistory(Base):
    __tablename__ = "article_price_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("article.id"), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    source: Mapped[str | None] = mapped_column(String, nullable=True)
    recorded_at: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_article_price_history_lookup", "article_id", "recorded_at"),
    )
