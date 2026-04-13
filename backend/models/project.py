import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import ForeignKey, Text, Numeric, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from .base import Base, ProjectStatus, LineCategory


class Project(Base):
    __tablename__ = "project"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("firm.id"), nullable=False)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customer.id"), nullable=False)
    quote_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("quote.id"), nullable=True)
    job_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("job_type.id"), nullable=False)
    assigned_to: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(SAEnum(ProjectStatus, name="project_status", create_constraint=False, native_enum=False), nullable=False, default=ProjectStatus.planned)
    planned_hours: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    actual_hours: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    planned_cost: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    actual_cost: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    margin_pct: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    line_items: Mapped[list["ProjectLineItem"]] = relationship(back_populates="project")


class ProjectLineItem(Base):
    __tablename__ = "project_line_item"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("project.id"), nullable=False)
    quote_line_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("quote_line_item.id"), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[LineCategory] = mapped_column(SAEnum(LineCategory, name="line_category", create_constraint=False, native_enum=False), nullable=False)
    actual_quantity: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    actual_unit_price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    actual_total: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    logged_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    logged_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    project: Mapped["Project"] = relationship(back_populates="line_items")
