import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, Index, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, JSONB
from .base import Base, EventType, EventEntityType


class Event(Base):
    __tablename__ = "event"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type: Mapped[EventEntityType] = mapped_column(SAEnum(EventEntityType, name="event_entity_type", create_constraint=False, native_enum=False), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    event_type: Mapped[EventType] = mapped_column(SAEnum(EventType, name="event_type", create_constraint=False, native_enum=False), nullable=False)
    actor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_event_entity", "entity_type", "entity_id"),
        Index("idx_event_actor", "actor_id"),
        Index("idx_event_time", "created_at"),
    )
