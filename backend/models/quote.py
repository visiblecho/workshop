import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Integer, ForeignKey, Text, Numeric, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from .base import Base, QuoteStatus, LineCategory, Unit


class Quote(Base):
    __tablename__ = "quote"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("firm.id"), nullable=False)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customer.id"), nullable=False)
    job_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("job_type.id"), nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    status: Mapped[QuoteStatus] = mapped_column(SAEnum(QuoteStatus, name="quote_status", create_constraint=False, native_enum=False), nullable=False, default=QuoteStatus.draft)
    total_net: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    total_gross: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    margin_target: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    cl_margin_pred: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    cl_price_bench: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    accepted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    rejected_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    line_items: Mapped[list["QuoteLineItem"]] = relationship(back_populates="quote")


class QuoteLineItem(Base):
    __tablename__ = "quote_line_item"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quote_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("quote.id"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[LineCategory] = mapped_column(SAEnum(LineCategory, name="line_category", create_constraint=False, native_enum=False), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    unit: Mapped[Unit] = mapped_column(SAEnum(Unit, name="unit", create_constraint=False, native_enum=False), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    article_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("article.id"), nullable=True)
    cl_price_flag: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    quote: Mapped["Quote"] = relationship(back_populates="line_items")
