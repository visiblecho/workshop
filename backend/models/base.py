import enum
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# --- Enums ---

class Segment(str, enum.Enum):
    shk = "shk"
    elektro = "elektro"
    dach_holz = "dach_holz"
    metallbau = "metallbau"
    geruestbau = "geruestbau"
    landschaftsbau = "landschaftsbau"
    general = "general"


class Role(str, enum.Enum):
    meister = "meister"
    geselle = "geselle"
    buero = "buero"


class CustomerType(str, enum.Enum):
    residential = "residential"
    commercial = "commercial"
    public = "public"


class QuoteStatus(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    accepted = "accepted"
    rejected = "rejected"
    expired = "expired"


class ProjectStatus(str, enum.Enum):
    planned = "planned"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class LineCategory(str, enum.Enum):
    labor = "labor"
    material = "material"
    other = "other"


class Unit(str, enum.Enum):
    hours = "hours"
    pieces = "pieces"
    meters = "meters"
    kg = "kg"
    liters = "liters"
    sqm = "sqm"
    flat_rate = "flat_rate"


class CLMetric(str, enum.Enum):
    duration_h = "duration_h"
    margin_pct = "margin_pct"
    material_cost = "material_cost"
    quote_total = "quote_total"
    conversion_rate = "conversion_rate"


class EventType(str, enum.Enum):
    created = "created"
    updated = "updated"
    status_changed = "status_changed"
    deleted = "deleted"


class EventEntityType(str, enum.Enum):
    quote = "quote"
    quote_line_item = "quote_line_item"
    project = "project"
    project_line_item = "project_line_item"
