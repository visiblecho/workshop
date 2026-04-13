from fastapi import APIRouter, Depends
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from database import get_db
from models.core import Firm, User, Customer
from models.quote import Quote
from models.project import Project
from models.cl import CLBenchmark, FirmBenchmark
from models.reference import JobType
from models.base import QuoteStatus, ProjectStatus, CLMetric

router = APIRouter(prefix="/api", tags=["firms"])


@router.get("/firms")
async def list_firms(db: Session = Depends(get_db)):
    firms = db.query(Firm).filter(Firm.deleted_at.is_(None)).all()
    return [
        {
            "id": str(f.id),
            "name": f.name,
            "segment": f.segment.value,
            "region": f.region,
            "employee_count": f.employee_count,
        }
        for f in firms
    ]


@router.get("/firms/{firm_id}/users")
async def list_users(firm_id: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.firm_id == firm_id, User.deleted_at.is_(None)).all()
    return [
        {
            "id": str(u.id),
            "firm_id": str(u.firm_id),
            "name": u.name,
            "role": u.role.value,
            "email": u.email,
            "language": u.language,
        }
        for u in users
    ]


@router.get("/firms/{firm_id}/dashboard")
async def dashboard(firm_id: str, db: Session = Depends(get_db)):
    firm = db.query(Firm).filter(Firm.id == firm_id).first()
    if not firm:
        return {"error": "Firm not found"}

    # Counts
    open_quotes = db.query(func.count(Quote.id)).filter(
        Quote.firm_id == firm_id, Quote.deleted_at.is_(None),
        Quote.status.in_([QuoteStatus.draft, QuoteStatus.sent]),
    ).scalar()

    active_projects = db.query(func.count(Project.id)).filter(
        Project.firm_id == firm_id, Project.deleted_at.is_(None),
        Project.status.in_([ProjectStatus.planned, ProjectStatus.active]),
    ).scalar()

    completed_projects = db.query(func.count(Project.id)).filter(
        Project.firm_id == firm_id, Project.deleted_at.is_(None),
        Project.status == ProjectStatus.completed,
    ).scalar()

    # Recent quotes
    recent_quotes = (
        db.query(Quote, Customer.name.label("customer_name"), JobType.name.label("job_type_name"))
        .join(Customer, Quote.customer_id == Customer.id)
        .join(JobType, Quote.job_type_id == JobType.id)
        .filter(Quote.firm_id == firm_id, Quote.deleted_at.is_(None))
        .order_by(Quote.created_at.desc())
        .limit(10)
        .all()
    )

    # Recent projects
    recent_projects = (
        db.query(Project, Customer.name.label("customer_name"), JobType.name.label("job_type_name"))
        .join(Customer, Project.customer_id == Customer.id)
        .join(JobType, Project.job_type_id == JobType.id)
        .filter(Project.firm_id == firm_id, Project.deleted_at.is_(None))
        .order_by(Project.created_at.desc())
        .limit(10)
        .all()
    )

    # CL insights: FirmBenchmark vs CLBenchmark for duration_h
    firm_benchmarks = (
        db.query(FirmBenchmark, JobType.name.label("job_type_name"))
        .join(JobType, FirmBenchmark.job_type_id == JobType.id)
        .filter(
            FirmBenchmark.firm_id == firm_id,
            FirmBenchmark.metric == CLMetric.duration_h,
        )
        .all()
    )

    cl_insights = []
    for fb, jt_name in firm_benchmarks:
        cl = db.query(CLBenchmark).filter(
            CLBenchmark.job_type_id == fb.job_type_id,
            CLBenchmark.metric == CLMetric.duration_h,
            CLBenchmark.segment == firm.segment,
        ).first()
        cl_insights.append({
            "job_type": jt_name,
            "firm_median": float(fb.p50) if fb.p50 else None,
            "platform_median": float(cl.p50) if cl else None,
            "platform_sample_size": cl.sample_size if cl else None,
        })

    # Customer/project/position counts for import narrative
    customer_count = db.query(func.count(Customer.id)).filter(
        Customer.firm_id == firm_id, Customer.deleted_at.is_(None),
    ).scalar()

    from models.quote import QuoteLineItem
    position_count = (
        db.query(func.count(QuoteLineItem.id))
        .join(Quote, QuoteLineItem.quote_id == Quote.id)
        .filter(Quote.firm_id == firm_id, QuoteLineItem.deleted_at.is_(None))
        .scalar()
    )

    return {
        "firm": {
            "id": str(firm.id),
            "name": firm.name,
            "segment": firm.segment.value,
            "region": firm.region,
        },
        "counts": {
            "open_quotes": open_quotes,
            "active_projects": active_projects,
            "completed_projects": completed_projects,
            "customers": customer_count,
            "positions": position_count,
        },
        "recent_quotes": [
            {
                "id": str(q.id),
                "customer_name": cname,
                "job_type": jname,
                "status": q.status.value,
                "total_net": float(q.total_net) if q.total_net else None,
                "created_at": q.created_at.isoformat() if q.created_at else None,
            }
            for q, cname, jname in recent_quotes
        ],
        "recent_projects": [
            {
                "id": str(p.id),
                "customer_name": cname,
                "job_type": jname,
                "status": p.status.value,
                "planned_hours": float(p.planned_hours) if p.planned_hours else None,
                "actual_hours": float(p.actual_hours) if p.actual_hours else None,
                "margin_pct": float(p.margin_pct) if p.margin_pct else None,
                "completed_at": p.completed_at.isoformat() if p.completed_at else None,
            }
            for p, cname, jname in recent_projects
        ],
        "cl_insights": cl_insights,
    }
