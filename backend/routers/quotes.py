import uuid
from datetime import datetime, timezone
from decimal import Decimal
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.quote import Quote, QuoteLineItem
from models.reference import JobType, Article
from models.event import Event
from models.cl import CLBenchmark, FirmBenchmark, ArticlePriceHistory
from models.core import Firm, User, Customer
from models.base import (
    QuoteStatus, LineCategory, Unit, CLMetric,
    EventType, EventEntityType, Segment,
)
from services.quote_service import generate_quote_ai, get_article_catalog, FALLBACK_QUOTE

router = APIRouter(prefix="/api", tags=["quotes"])


class GenerateRequest(BaseModel):
    firm_id: str
    customer_id: str
    job_type_id: str
    description: str
    created_by: str


@router.post("/quotes/generate")
async def generate_quote(req: GenerateRequest, db: Session = Depends(get_db)):
    job_type = db.query(JobType).filter(JobType.id == req.job_type_id).first()
    if not job_type:
        return {"error": "Job type not found"}

    catalog = get_article_catalog(db)
    result = await generate_quote_ai(req.description, job_type.name, catalog)
    is_fallback = result is FALLBACK_QUOTE

    # Calculate totals
    line_items = result.get("line_items", [])
    total_net = Decimal(str(sum(item.get("total", 0) for item in line_items)))
    total_gross = round(total_net * Decimal("1.19"), 2)

    # Get CL predictions
    firm = db.query(Firm).filter(Firm.id == req.firm_id).first()
    cl_margin = None
    cl_price = None
    cl = db.query(CLBenchmark).filter(
        CLBenchmark.job_type_id == req.job_type_id,
        CLBenchmark.metric == CLMetric.margin_pct,
        CLBenchmark.segment == (firm.segment if firm else Segment.shk),
    ).first()
    if cl:
        cl_margin = cl.p50
    cl_price = db.query(CLBenchmark).filter(
        CLBenchmark.job_type_id == req.job_type_id,
        CLBenchmark.metric == CLMetric.quote_total,
        CLBenchmark.segment == (firm.segment if firm else Segment.shk),
    ).first()

    # Save quote
    quote = Quote(
        id=uuid.uuid4(),
        firm_id=req.firm_id,
        customer_id=req.customer_id,
        job_type_id=req.job_type_id,
        created_by=req.created_by,
        status=QuoteStatus.draft,
        total_net=Decimal(str(total_net)),
        total_gross=Decimal(str(total_gross)),
        margin_target=Decimal("25"),
        cl_margin_pred=cl_margin,
        cl_price_bench=Decimal(str(float(cl_price.p50))) if cl_price else None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(quote)

    saved_items = []
    for item in line_items:
        art_id = item.get("article_id")
        if art_id:
            try:
                uuid.UUID(art_id)
            except (ValueError, TypeError):
                art_id = None
        qli = QuoteLineItem(
            id=uuid.uuid4(),
            quote_id=quote.id,
            position=item.get("position", 0),
            description=item.get("description", ""),
            category=LineCategory(item.get("category", "labor")),
            quantity=Decimal(str(item.get("quantity", 0))),
            unit=Unit(item.get("unit", "pieces")),
            unit_price=Decimal(str(item.get("unit_price", 0))),
            total=Decimal(str(item.get("total", 0))),
            article_id=art_id,
        )
        db.add(qli)
        saved_items.append(qli)

    # Event
    event = Event(
        id=uuid.uuid4(),
        entity_type=EventEntityType.quote,
        entity_id=quote.id,
        event_type=EventType.created,
        actor_id=req.created_by,
        payload={"total_net": str(total_net), "description": req.description},
        created_at=datetime.now(timezone.utc),
    )
    db.add(event)
    db.commit()

    return {
        "quote_id": str(quote.id),
        "is_fallback": is_fallback,
        "total_net": float(total_net),
        "total_gross": float(total_gross),
        "line_items": [
            {
                "id": str(qli.id),
                "position": qli.position,
                "description": qli.description,
                "category": qli.category.value,
                "quantity": float(qli.quantity),
                "unit": qli.unit.value,
                "unit_price": float(qli.unit_price),
                "total": float(qli.total),
                "article_id": str(qli.article_id) if qli.article_id else None,
            }
            for qli in saved_items
        ],
    }


@router.get("/benchmarks/{job_type_id}")
async def get_benchmarks(job_type_id: str, firm_id: str = "", db: Session = Depends(get_db)):
    firm = db.query(Firm).filter(Firm.id == firm_id).first() if firm_id else None
    segment = firm.segment if firm else Segment.shk

    # CL benchmarks
    cl_benchmarks = db.query(CLBenchmark).filter(
        CLBenchmark.job_type_id == job_type_id,
        CLBenchmark.segment == segment,
    ).all()

    cl_data = {}
    for cl in cl_benchmarks:
        cl_data[cl.metric.value] = {
            "p25": float(cl.p25), "p50": float(cl.p50),
            "p75": float(cl.p75), "mean": float(cl.mean),
            "sample_size": cl.sample_size,
        }

    # Firm benchmarks
    fb_data = {}
    if firm_id:
        firm_benchmarks = db.query(FirmBenchmark).filter(
            FirmBenchmark.firm_id == firm_id,
            FirmBenchmark.job_type_id == job_type_id,
        ).all()
        for fb in firm_benchmarks:
            fb_data[fb.metric.value] = {
                "p50": float(fb.p50) if fb.p50 else None,
                "mean": float(fb.mean),
                "sample_size": fb.sample_size,
            }

    return {
        "job_type_id": job_type_id,
        "firm_id": firm_id,
        "cl_benchmarks": cl_data,
        "firm_benchmarks": fb_data,
    }


@router.get("/articles/{article_id}/price-history")
async def get_price_history(article_id: str, db: Session = Depends(get_db)):
    records = (
        db.query(ArticlePriceHistory)
        .filter(ArticlePriceHistory.article_id == article_id)
        .order_by(ArticlePriceHistory.recorded_at.desc())
        .all()
    )
    return [
        {
            "price": float(r.price),
            "currency": r.currency,
            "source": r.source,
            "recorded_at": r.recorded_at.isoformat(),
        }
        for r in records
    ]


@router.get("/events")
async def get_events(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    events = (
        db.query(Event, User.name.label("actor_name"), User.role.label("actor_role"))
        .join(User, Event.actor_id == User.id)
        .filter(Event.entity_type == entity_type, Event.entity_id == entity_id)
        .order_by(Event.created_at.desc())
        .all()
    )
    return [
        {
            "id": str(e.id),
            "event_type": e.event_type.value,
            "actor_name": actor_name,
            "actor_role": actor_role.value,
            "payload": e.payload,
            "created_at": e.created_at.isoformat(),
        }
        for e, actor_name, actor_role in events
    ]


@router.get("/firms/{firm_id}/customers")
async def list_customers(firm_id: str, db: Session = Depends(get_db)):
    customers = db.query(Customer).filter(
        Customer.firm_id == firm_id, Customer.deleted_at.is_(None),
    ).all()
    return [
        {"id": str(c.id), "name": c.name, "type": c.type.value}
        for c in customers
    ]


@router.get("/firms/{firm_id}/job-types")
async def list_job_types(firm_id: str, db: Session = Depends(get_db)):
    firm = db.query(Firm).filter(Firm.id == firm_id).first()
    segment = firm.segment if firm else Segment.shk
    job_types = db.query(JobType).filter(
        JobType.segment == segment, JobType.deleted_at.is_(None),
    ).all()
    return [
        {"id": str(jt.id), "name": jt.name, "description": jt.description}
        for jt in job_types
    ]


@router.get("/projects/{project_id}")
async def get_project(project_id: str, db: Session = Depends(get_db)):
    from models.project import Project, ProjectLineItem
    from models.quote import QuoteLineItem

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return {"error": "Project not found"}

    customer = db.query(Customer).filter(Customer.id == project.customer_id).first()
    job_type = db.query(JobType).filter(JobType.id == project.job_type_id).first()

    # Project line items with linked quote line items
    plis = db.query(ProjectLineItem).filter(
        ProjectLineItem.project_id == project_id,
        ProjectLineItem.deleted_at.is_(None),
    ).all()

    line_items = []
    for pli in plis:
        quoted = None
        if pli.quote_line_id:
            qli = db.query(QuoteLineItem).filter(QuoteLineItem.id == pli.quote_line_id).first()
            if qli:
                quoted = {
                    "description": qli.description,
                    "quantity": float(qli.quantity),
                    "unit_price": float(qli.unit_price),
                    "total": float(qli.total),
                }
        line_items.append({
            "id": str(pli.id),
            "description": pli.description,
            "category": pli.category.value,
            "actual_quantity": float(pli.actual_quantity),
            "actual_unit_price": float(pli.actual_unit_price),
            "actual_total": float(pli.actual_total),
            "notes": pli.notes,
            "quoted": quoted,
        })

    # Benchmarks
    firm = db.query(Firm).filter(Firm.id == project.firm_id).first()
    fb = db.query(FirmBenchmark).filter(
        FirmBenchmark.firm_id == project.firm_id,
        FirmBenchmark.job_type_id == project.job_type_id,
        FirmBenchmark.metric == CLMetric.duration_h,
    ).first()
    cl = db.query(CLBenchmark).filter(
        CLBenchmark.job_type_id == project.job_type_id,
        CLBenchmark.metric == CLMetric.duration_h,
        CLBenchmark.segment == (firm.segment if firm else Segment.shk),
    ).first()

    return {
        "id": str(project.id),
        "customer_name": customer.name if customer else "",
        "job_type": job_type.name if job_type else "",
        "status": project.status.value,
        "planned_hours": float(project.planned_hours) if project.planned_hours else None,
        "actual_hours": float(project.actual_hours) if project.actual_hours else None,
        "planned_cost": float(project.planned_cost) if project.planned_cost else None,
        "actual_cost": float(project.actual_cost) if project.actual_cost else None,
        "margin_pct": float(project.margin_pct) if project.margin_pct else None,
        "started_at": project.started_at.isoformat() if project.started_at else None,
        "completed_at": project.completed_at.isoformat() if project.completed_at else None,
        "line_items": line_items,
        "firm_benchmark_duration": float(fb.p50) if fb and fb.p50 else None,
        "cl_benchmark_duration": float(cl.p50) if cl else None,
        "cl_sample_size": cl.sample_size if cl else None,
    }
