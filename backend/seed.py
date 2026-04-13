"""
Seed script for Workshop prototype.
Idempotent: uses merge (upsert) so it can be re-run safely.

Usage: python seed.py
"""

import uuid
from datetime import datetime, date, timedelta, timezone
from decimal import Decimal
from database import SessionLocal, engine
from models import Base
from models.core import Firm, User, Customer
from models.reference import JobType, Article
from models.quote import Quote, QuoteLineItem
from models.project import Project, ProjectLineItem
from models.event import Event
from models.cl import CLBenchmark, FirmBenchmark, ArticlePriceHistory
from models.base import (
    Segment, Role, CustomerType, QuoteStatus, ProjectStatus,
    LineCategory, Unit, CLMetric, EventType, EventEntityType,
)

# ============================================================
# Fixed UUIDs for referential integrity
# ============================================================

# Firms
WEBER_FIRM_ID = uuid.UUID("10000000-0000-0000-0000-000000000001")
NEUER_FIRM_ID = uuid.UUID("10000000-0000-0000-0000-000000000002")

# Users (Weber firm)
MEISTER_WEBER_ID = uuid.UUID("20000000-0000-0000-0000-000000000001")
GESELLE_HOFFMANN_ID = uuid.UUID("20000000-0000-0000-0000-000000000002")
BUERO_YILMAZ_ID = uuid.UUID("20000000-0000-0000-0000-000000000003")

# Customers
CUSTOMER_MUELLER_ID = uuid.UUID("30000000-0000-0000-0000-000000000001")
CUSTOMER_SCHMIDT_ID = uuid.UUID("30000000-0000-0000-0000-000000000002")
CUSTOMER_FISCHER_ID = uuid.UUID("30000000-0000-0000-0000-000000000003")
CUSTOMER_WAGNER_ID = uuid.UUID("30000000-0000-0000-0000-000000000004")
CUSTOMER_BECKER_ID = uuid.UUID("30000000-0000-0000-0000-000000000005")

# Job Types
JT_HEIZUNGSTAUSCH_ID = uuid.UUID("40000000-0000-0000-0000-000000000001")
JT_BADSANIERUNG_ID = uuid.UUID("40000000-0000-0000-0000-000000000002")
JT_WARTUNG_ID = uuid.UUID("40000000-0000-0000-0000-000000000003")
JT_ROHRBRUCH_ID = uuid.UUID("40000000-0000-0000-0000-000000000004")
JT_WAERMEPUMPE_ID = uuid.UUID("40000000-0000-0000-0000-000000000005")

# Articles (first 10 with fixed IDs for quote line items)
ART_KUPFERROHR_15 = uuid.UUID("50000000-0000-0000-0000-000000000001")
ART_KUPFERROHR_22 = uuid.UUID("50000000-0000-0000-0000-000000000002")
ART_HEIZKOERPER_22 = uuid.UUID("50000000-0000-0000-0000-000000000003")
ART_THERMOSTATVENTIL = uuid.UUID("50000000-0000-0000-0000-000000000004")
ART_UMWAELZPUMPE = uuid.UUID("50000000-0000-0000-0000-000000000005")
ART_GASBRENNWERT = uuid.UUID("50000000-0000-0000-0000-000000000006")
ART_WAERMEPUMPE = uuid.UUID("50000000-0000-0000-0000-000000000007")
ART_AUSDEHNUNG = uuid.UUID("50000000-0000-0000-0000-000000000008")
ART_PRESSFITTING_15 = uuid.UUID("50000000-0000-0000-0000-000000000009")
ART_PRESSFITTING_22 = uuid.UUID("50000000-0000-0000-0000-00000000000a")
ART_ROHR_ISOLATION = uuid.UUID("50000000-0000-0000-0000-00000000000b")
ART_ABSPERRHAHN = uuid.UUID("50000000-0000-0000-0000-00000000000c")
ART_FLEXSCHLAUCH = uuid.UUID("50000000-0000-0000-0000-00000000000d")
ART_DICHTBAND = uuid.UUID("50000000-0000-0000-0000-00000000000e")
ART_SILIKON = uuid.UUID("50000000-0000-0000-0000-00000000000f")
ART_WANNENANKER = uuid.UUID("50000000-0000-0000-0000-000000000010")
ART_DUSCHARMATUR = uuid.UUID("50000000-0000-0000-0000-000000000011")
ART_WASCHTISCH = uuid.UUID("50000000-0000-0000-0000-000000000012")
ART_WC_ELEMENT = uuid.UUID("50000000-0000-0000-0000-000000000013")
ART_FLIESEN_KLEBER = uuid.UUID("50000000-0000-0000-0000-000000000014")
ART_ABFLUSSROHR = uuid.UUID("50000000-0000-0000-0000-000000000015")
ART_SIPHON = uuid.UUID("50000000-0000-0000-0000-000000000016")
ART_PANZERSCHLAUCH = uuid.UUID("50000000-0000-0000-0000-000000000017")
ART_ECKVENTIL = uuid.UUID("50000000-0000-0000-0000-000000000018")
ART_HEIZUNGSPUMPE_E = uuid.UUID("50000000-0000-0000-0000-000000000019")

# Quotes
QUOTE_IDS = [uuid.UUID(f"60000000-0000-0000-0000-00000000000{i}") for i in range(1, 9)]

# Projects
PROJECT_IDS = [uuid.UUID(f"70000000-0000-0000-0000-00000000000{i}") for i in range(1, 9)]

NOW = datetime.now(timezone.utc)


def seed_reference_data(session):
    """E0-S3: Firms, users, customers, job types, articles."""

    # --- Firms ---
    firms = [
        Firm(
            id=WEBER_FIRM_ID, name="Weber Haustechnik GmbH",
            segment=Segment.shk, country="DE", currency="EUR",
            region="Niedersachsen", postal_code="30159",
            employee_count=4,
        ),
        Firm(
            id=NEUER_FIRM_ID, name="Neuer Betrieb",
            segment=Segment.shk, country="DE", currency="EUR",
            region="Niedersachsen", postal_code="30159",
            employee_count=1,
        ),
    ]
    for f in firms:
        session.merge(f)

    # --- Users (Weber firm) ---
    users = [
        User(
            id=MEISTER_WEBER_ID, firm_id=WEBER_FIRM_ID,
            name="Thomas Weber", role=Role.meister,
            email="weber@weber-haustechnik.de", language="de",
        ),
        User(
            id=GESELLE_HOFFMANN_ID, firm_id=WEBER_FIRM_ID,
            name="Marco Hoffmann", role=Role.geselle,
            email="hoffmann@weber-haustechnik.de", language="de",
        ),
        User(
            id=BUERO_YILMAZ_ID, firm_id=WEBER_FIRM_ID,
            name="Elif Yilmaz", role=Role.buero,
            email="yilmaz@weber-haustechnik.de", language="de",
        ),
    ]
    for u in users:
        session.merge(u)

    # --- Customers ---
    customers = [
        Customer(
            id=CUSTOMER_MUELLER_ID, firm_id=WEBER_FIRM_ID,
            name="Familie Müller", type=CustomerType.residential,
            address="Lister Meile 42, 30161 Hannover",
            postal_code="30161", phone="0511-555-0101",
        ),
        Customer(
            id=CUSTOMER_SCHMIDT_ID, firm_id=WEBER_FIRM_ID,
            name="Schmidt Immobilien GmbH", type=CustomerType.commercial,
            address="Jungfernstieg 12, 20354 Hamburg",
            postal_code="20354", phone="040-555-0202",
        ),
        Customer(
            id=CUSTOMER_FISCHER_ID, firm_id=WEBER_FIRM_ID,
            name="Herr Fischer", type=CustomerType.residential,
            address="Jasperallee 7, 38102 Braunschweig",
            postal_code="38102", phone="0531-555-0303",
        ),
        Customer(
            id=CUSTOMER_WAGNER_ID, firm_id=WEBER_FIRM_ID,
            name="Ehepaar Wagner", type=CustomerType.residential,
            address="Am Lindener Berge 15, 30449 Hannover",
            postal_code="30449", phone="0511-555-0404",
        ),
        Customer(
            id=CUSTOMER_BECKER_ID, firm_id=WEBER_FIRM_ID,
            name="Becker & Söhne KG", type=CustomerType.commercial,
            address="Hildesheimer Str. 265, 30519 Hannover",
            postal_code="30519", phone="0511-555-0505",
        ),
    ]
    for c in customers:
        session.merge(c)

    # --- Job Types ---
    job_types = [
        JobType(
            id=JT_HEIZUNGSTAUSCH_ID, segment=Segment.shk,
            name="Heizungstausch",
            description="Austausch einer bestehenden Heizungsanlage (Gas, Öl) gegen neue Anlage",
            avg_duration_h=Decimal("16"), avg_margin_pct=Decimal("24"), sample_size=342,
        ),
        JobType(
            id=JT_BADSANIERUNG_ID, segment=Segment.shk,
            name="Badsanierung",
            description="Komplettsanierung oder Teilsanierung eines Badezimmers",
            avg_duration_h=Decimal("12"), avg_margin_pct=Decimal("26"), sample_size=518,
        ),
        JobType(
            id=JT_WARTUNG_ID, segment=Segment.shk,
            name="Wartung",
            description="Regelmäßige Wartung von Heizungsanlagen und Sanitärinstallationen",
            avg_duration_h=Decimal("3"), avg_margin_pct=Decimal("35"), sample_size=1240,
        ),
        JobType(
            id=JT_ROHRBRUCH_ID, segment=Segment.shk,
            name="Rohrbruch-Reparatur",
            description="Notfall-Reparatur bei Rohrbruch inkl. Leckortung",
            avg_duration_h=Decimal("5"), avg_margin_pct=Decimal("30"), sample_size=287,
        ),
        JobType(
            id=JT_WAERMEPUMPE_ID, segment=Segment.shk,
            name="Wärmepumpe-Installation",
            description="Neuinstallation einer Wärmepumpe (Luft-Wasser oder Sole)",
            avg_duration_h=Decimal("24"), avg_margin_pct=Decimal("22"), sample_size=156,
        ),
    ]
    for jt in job_types:
        session.merge(jt)

    # --- Articles (25 SHK materials) ---
    articles = [
        Article(id=ART_KUPFERROHR_15, segment=Segment.shk, name="Kupferrohr 15mm (Stange 5m)", datanorm_id="DN-CU15-500", unit=Unit.meters, default_price=Decimal("8.50"), wholesaler="Richter+Frenzel", last_price_date=date(2026, 4, 1)),
        Article(id=ART_KUPFERROHR_22, segment=Segment.shk, name="Kupferrohr 22mm (Stange 5m)", datanorm_id="DN-CU22-500", unit=Unit.meters, default_price=Decimal("12.80"), wholesaler="Richter+Frenzel", last_price_date=date(2026, 4, 1)),
        Article(id=ART_HEIZKOERPER_22, segment=Segment.shk, name="Flachheizkörper Typ 22 (600x1000)", datanorm_id="DN-FK22-610", unit=Unit.pieces, default_price=Decimal("289.00"), wholesaler="Buderus", last_price_date=date(2026, 3, 15)),
        Article(id=ART_THERMOSTATVENTIL, segment=Segment.shk, name="Thermostatventil-Set DN15", datanorm_id="DN-TV15-SET", unit=Unit.pieces, default_price=Decimal("34.50"), wholesaler="Oventrop", last_price_date=date(2026, 3, 20)),
        Article(id=ART_UMWAELZPUMPE, segment=Segment.shk, name="Umwälzpumpe Hocheffizienz 25-60", datanorm_id="DN-UP2560", unit=Unit.pieces, default_price=Decimal("385.00"), wholesaler="Grundfos", last_price_date=date(2026, 3, 1)),
        Article(id=ART_GASBRENNWERT, segment=Segment.shk, name="Gas-Brennwertgerät 24kW", datanorm_id="DN-GBW24", unit=Unit.pieces, default_price=Decimal("3200.00"), wholesaler="Viessmann", last_price_date=date(2026, 2, 15)),
        Article(id=ART_WAERMEPUMPE, segment=Segment.shk, name="Luft-Wasser-Wärmepumpe 8kW", datanorm_id="DN-LWWP8", unit=Unit.pieces, default_price=Decimal("8500.00"), wholesaler="Viessmann", last_price_date=date(2026, 3, 1)),
        Article(id=ART_AUSDEHNUNG, segment=Segment.shk, name="Ausdehnungsgefäß 35L", datanorm_id="DN-ADG35", unit=Unit.pieces, default_price=Decimal("125.00"), wholesaler="Flamco", last_price_date=date(2026, 3, 10)),
        Article(id=ART_PRESSFITTING_15, segment=Segment.shk, name="Pressfitting T-Stück 15mm", datanorm_id="DN-PF15T", unit=Unit.pieces, default_price=Decimal("6.20"), wholesaler="Viega", last_price_date=date(2026, 4, 1)),
        Article(id=ART_PRESSFITTING_22, segment=Segment.shk, name="Pressfitting T-Stück 22mm", datanorm_id="DN-PF22T", unit=Unit.pieces, default_price=Decimal("9.80"), wholesaler="Viega", last_price_date=date(2026, 4, 1)),
        Article(id=ART_ROHR_ISOLATION, segment=Segment.shk, name="Rohrisolierung 22mm (2m)", datanorm_id="DN-ISO22-200", unit=Unit.meters, default_price=Decimal("4.50"), wholesaler="Armacell", last_price_date=date(2026, 3, 15)),
        Article(id=ART_ABSPERRHAHN, segment=Segment.shk, name="Absperrhahn Kugel DN20", datanorm_id="DN-AH-K20", unit=Unit.pieces, default_price=Decimal("18.90"), wholesaler="Viega", last_price_date=date(2026, 3, 20)),
        Article(id=ART_FLEXSCHLAUCH, segment=Segment.shk, name="Flexschlauch 3/4\" 500mm", datanorm_id="DN-FLEX34-500", unit=Unit.pieces, default_price=Decimal("12.50"), wholesaler="Sanitop", last_price_date=date(2026, 3, 10)),
        Article(id=ART_DICHTBAND, segment=Segment.shk, name="Dichtband PTFE 12mm x 12m", datanorm_id="DN-PTFE-1212", unit=Unit.pieces, default_price=Decimal("2.80"), wholesaler="diverse", last_price_date=date(2026, 1, 1)),
        Article(id=ART_SILIKON, segment=Segment.shk, name="Sanitär-Silikon weiß 310ml", datanorm_id="DN-SIL-W310", unit=Unit.pieces, default_price=Decimal("7.90"), wholesaler="Soudal", last_price_date=date(2026, 2, 1)),
        Article(id=ART_WANNENANKER, segment=Segment.shk, name="Wannenanker-Set Universal", datanorm_id="DN-WA-UNI", unit=Unit.pieces, default_price=Decimal("24.50"), wholesaler="Kaldewei", last_price_date=date(2026, 3, 1)),
        Article(id=ART_DUSCHARMATUR, segment=Segment.shk, name="Duscharmatur Unterputz Thermostat", datanorm_id="DN-DA-UPT", unit=Unit.pieces, default_price=Decimal("245.00"), wholesaler="Hansgrohe", last_price_date=date(2026, 3, 15)),
        Article(id=ART_WASCHTISCH, segment=Segment.shk, name="Waschtisch 60cm weiß", datanorm_id="DN-WT60-W", unit=Unit.pieces, default_price=Decimal("159.00"), wholesaler="Duravit", last_price_date=date(2026, 3, 1)),
        Article(id=ART_WC_ELEMENT, segment=Segment.shk, name="WC-Vorwandelement 112cm", datanorm_id="DN-VWE112", unit=Unit.pieces, default_price=Decimal("189.00"), wholesaler="Geberit", last_price_date=date(2026, 3, 10)),
        Article(id=ART_FLIESEN_KLEBER, segment=Segment.shk, name="Fliesenkleber flexibel 25kg", datanorm_id="DN-FK-FLEX25", unit=Unit.kg, default_price=Decimal("0.95"), wholesaler="PCI", last_price_date=date(2026, 2, 15)),
        Article(id=ART_ABFLUSSROHR, segment=Segment.shk, name="HT-Rohr DN50 1m", datanorm_id="DN-HT50-100", unit=Unit.meters, default_price=Decimal("4.20"), wholesaler="Ostendorf", last_price_date=date(2026, 3, 1)),
        Article(id=ART_SIPHON, segment=Segment.shk, name="Röhren-Siphon 1 1/4\"", datanorm_id="DN-RS-114", unit=Unit.pieces, default_price=Decimal("15.80"), wholesaler="Viega", last_price_date=date(2026, 3, 15)),
        Article(id=ART_PANZERSCHLAUCH, segment=Segment.shk, name="Panzerschlauch 3/8\" 300mm", datanorm_id="DN-PS38-300", unit=Unit.pieces, default_price=Decimal("8.90"), wholesaler="Sanitop", last_price_date=date(2026, 3, 10)),
        Article(id=ART_ECKVENTIL, segment=Segment.shk, name="Eckventil 1/2\" x 3/8\"", datanorm_id="DN-EV-1238", unit=Unit.pieces, default_price=Decimal("11.50"), wholesaler="Schell", last_price_date=date(2026, 3, 20)),
        Article(id=ART_HEIZUNGSPUMPE_E, segment=Segment.shk, name="Hocheffizienzpumpe 25-40", datanorm_id="DN-HEP2540", unit=Unit.pieces, default_price=Decimal("320.00"), wholesaler="Wilo", last_price_date=date(2026, 3, 1)),
    ]
    for a in articles:
        session.merge(a)

    session.commit()
    print(f"  Reference data seeded: 2 firms, 3 users, 5 customers, 5 job types, {len(articles)} articles")


def seed_historical_data(session):
    """E0-S4: Projects, quotes, line items, events, benchmarks, price history."""

    # ============================================================
    # Helper dates (projects spread over last 6 months)
    # ============================================================
    def ago(days):
        return NOW - timedelta(days=days)

    # ============================================================
    # 8 Quotes (5 completed projects + 3 active)
    # ============================================================

    quotes_data = [
        # Completed projects (5)
        dict(id=QUOTE_IDS[0], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_MUELLER_ID,
             job_type_id=JT_BADSANIERUNG_ID, created_by=MEISTER_WEBER_ID,
             status=QuoteStatus.accepted, total_net=Decimal("8200"), total_gross=Decimal("9758"),
             margin_target=Decimal("25"), cl_margin_pred=Decimal("26"), cl_price_bench=Decimal("7800"),
             sent_at=ago(180), accepted_at=ago(175), created_at=ago(182)),
        dict(id=QUOTE_IDS[1], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_SCHMIDT_ID,
             job_type_id=JT_HEIZUNGSTAUSCH_ID, created_by=MEISTER_WEBER_ID,
             status=QuoteStatus.accepted, total_net=Decimal("12400"), total_gross=Decimal("14756"),
             margin_target=Decimal("25"), cl_margin_pred=Decimal("24"), cl_price_bench=Decimal("11800"),
             sent_at=ago(150), accepted_at=ago(145), created_at=ago(152)),
        dict(id=QUOTE_IDS[2], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_FISCHER_ID,
             job_type_id=JT_WARTUNG_ID, created_by=MEISTER_WEBER_ID,
             status=QuoteStatus.accepted, total_net=Decimal("450"), total_gross=Decimal("535.50"),
             margin_target=Decimal("35"), cl_margin_pred=Decimal("35"), cl_price_bench=Decimal("420"),
             sent_at=ago(120), accepted_at=ago(118), created_at=ago(122)),
        dict(id=QUOTE_IDS[3], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_WAGNER_ID,
             job_type_id=JT_BADSANIERUNG_ID, created_by=MEISTER_WEBER_ID,
             status=QuoteStatus.accepted, total_net=Decimal("11500"), total_gross=Decimal("13685"),
             margin_target=Decimal("25"), cl_margin_pred=Decimal("26"), cl_price_bench=Decimal("10800"),
             sent_at=ago(90), accepted_at=ago(85), created_at=ago(92)),
        dict(id=QUOTE_IDS[4], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_BECKER_ID,
             job_type_id=JT_HEIZUNGSTAUSCH_ID, created_by=MEISTER_WEBER_ID,
             status=QuoteStatus.accepted, total_net=Decimal("15800"), total_gross=Decimal("18802"),
             margin_target=Decimal("25"), cl_margin_pred=Decimal("24"), cl_price_bench=Decimal("14500"),
             sent_at=ago(60), accepted_at=ago(55), created_at=ago(62)),
        # Active projects (3)
        dict(id=QUOTE_IDS[5], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_MUELLER_ID,
             job_type_id=JT_WAERMEPUMPE_ID, created_by=MEISTER_WEBER_ID,
             status=QuoteStatus.accepted, total_net=Decimal("18500"), total_gross=Decimal("22015"),
             margin_target=Decimal("22"), cl_margin_pred=Decimal("22"), cl_price_bench=Decimal("17200"),
             sent_at=ago(30), accepted_at=ago(25), created_at=ago(32)),
        dict(id=QUOTE_IDS[6], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_FISCHER_ID,
             job_type_id=JT_ROHRBRUCH_ID, created_by=MEISTER_WEBER_ID,
             status=QuoteStatus.accepted, total_net=Decimal("1200"), total_gross=Decimal("1428"),
             margin_target=Decimal("30"), cl_margin_pred=Decimal("30"), cl_price_bench=Decimal("1100"),
             sent_at=ago(15), accepted_at=ago(14), created_at=ago(16)),
        dict(id=QUOTE_IDS[7], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_WAGNER_ID,
             job_type_id=JT_WARTUNG_ID, created_by=MEISTER_WEBER_ID,
             status=QuoteStatus.accepted, total_net=Decimal("380"), total_gross=Decimal("452.20"),
             margin_target=Decimal("35"), cl_margin_pred=Decimal("35"), cl_price_bench=Decimal("400"),
             sent_at=ago(10), accepted_at=ago(8), created_at=ago(12)),
    ]
    for q_data in quotes_data:
        session.merge(Quote(**q_data))

    # ============================================================
    # Quote Line Items
    # ============================================================

    qli_counter = 0
    def qli_id():
        nonlocal qli_counter
        qli_counter += 1
        return uuid.UUID(f"61000000-0000-0000-0000-{qli_counter:012d}")

    quote_line_items_all = []

    # Quote 0: Badsanierung Müller -- 5 items
    q0_items = [
        dict(quote_id=QUOTE_IDS[0], position=1, description="Demontage alte Sanitärobjekte", category=LineCategory.labor, quantity=Decimal("8"), unit=Unit.hours, unit_price=Decimal("58"), total=Decimal("464")),
        dict(quote_id=QUOTE_IDS[0], position=2, description="Waschtisch 60cm weiß", category=LineCategory.material, quantity=Decimal("1"), unit=Unit.pieces, unit_price=Decimal("159"), total=Decimal("159"), article_id=ART_WASCHTISCH),
        dict(quote_id=QUOTE_IDS[0], position=3, description="WC-Vorwandelement 112cm", category=LineCategory.material, quantity=Decimal("1"), unit=Unit.pieces, unit_price=Decimal("189"), total=Decimal("189"), article_id=ART_WC_ELEMENT),
        dict(quote_id=QUOTE_IDS[0], position=4, description="Duscharmatur Unterputz Thermostat", category=LineCategory.material, quantity=Decimal("1"), unit=Unit.pieces, unit_price=Decimal("245"), total=Decimal("245"), article_id=ART_DUSCHARMATUR),
        dict(quote_id=QUOTE_IDS[0], position=5, description="Installation und Anschlussarbeiten", category=LineCategory.labor, quantity=Decimal("16"), unit=Unit.hours, unit_price=Decimal("58"), total=Decimal("928")),
    ]

    # Quote 1: Heizungstausch Schmidt -- 6 items
    q1_items = [
        dict(quote_id=QUOTE_IDS[1], position=1, description="Demontage Altgerät inkl. Entsorgung", category=LineCategory.labor, quantity=Decimal("6"), unit=Unit.hours, unit_price=Decimal("58"), total=Decimal("348")),
        dict(quote_id=QUOTE_IDS[1], position=2, description="Gas-Brennwertgerät 24kW", category=LineCategory.material, quantity=Decimal("1"), unit=Unit.pieces, unit_price=Decimal("3200"), total=Decimal("3200"), article_id=ART_GASBRENNWERT),
        dict(quote_id=QUOTE_IDS[1], position=3, description="Kupferrohr 22mm", category=LineCategory.material, quantity=Decimal("15"), unit=Unit.meters, unit_price=Decimal("12.80"), total=Decimal("192"), article_id=ART_KUPFERROHR_22),
        dict(quote_id=QUOTE_IDS[1], position=4, description="Umwälzpumpe Hocheffizienz", category=LineCategory.material, quantity=Decimal("1"), unit=Unit.pieces, unit_price=Decimal("385"), total=Decimal("385"), article_id=ART_UMWAELZPUMPE),
        dict(quote_id=QUOTE_IDS[1], position=5, description="Ausdehnungsgefäß 35L", category=LineCategory.material, quantity=Decimal("1"), unit=Unit.pieces, unit_price=Decimal("125"), total=Decimal("125"), article_id=ART_AUSDEHNUNG),
        dict(quote_id=QUOTE_IDS[1], position=6, description="Installation und Inbetriebnahme", category=LineCategory.labor, quantity=Decimal("12"), unit=Unit.hours, unit_price=Decimal("58"), total=Decimal("696")),
    ]

    # Quote 2: Wartung Fischer -- 3 items
    q2_items = [
        dict(quote_id=QUOTE_IDS[2], position=1, description="Heizungswartung (Brenner, Filter, Dichtungen)", category=LineCategory.labor, quantity=Decimal("2.5"), unit=Unit.hours, unit_price=Decimal("62"), total=Decimal("155")),
        dict(quote_id=QUOTE_IDS[2], position=2, description="Verschleißteile (Dichtungen, Filter)", category=LineCategory.material, quantity=Decimal("1"), unit=Unit.flat_rate, unit_price=Decimal("45"), total=Decimal("45")),
        dict(quote_id=QUOTE_IDS[2], position=3, description="Abgasmessung und Protokoll", category=LineCategory.labor, quantity=Decimal("0.5"), unit=Unit.hours, unit_price=Decimal("62"), total=Decimal("31")),
    ]

    # Quote 3: Badsanierung Wagner -- 5 items (bigger job)
    q3_items = [
        dict(quote_id=QUOTE_IDS[3], position=1, description="Komplettdemontage Altbad", category=LineCategory.labor, quantity=Decimal("12"), unit=Unit.hours, unit_price=Decimal("58"), total=Decimal("696")),
        dict(quote_id=QUOTE_IDS[3], position=2, description="Waschtisch + WC + Dusche komplett", category=LineCategory.material, quantity=Decimal("1"), unit=Unit.flat_rate, unit_price=Decimal("2800"), total=Decimal("2800")),
        dict(quote_id=QUOTE_IDS[3], position=3, description="Fliesen und Abdichtung", category=LineCategory.material, quantity=Decimal("18"), unit=Unit.sqm, unit_price=Decimal("85"), total=Decimal("1530")),
        dict(quote_id=QUOTE_IDS[3], position=4, description="Rohinstallation Wasser/Abwasser", category=LineCategory.labor, quantity=Decimal("14"), unit=Unit.hours, unit_price=Decimal("58"), total=Decimal("812")),
        dict(quote_id=QUOTE_IDS[3], position=5, description="Montage und Endanschluss", category=LineCategory.labor, quantity=Decimal("16"), unit=Unit.hours, unit_price=Decimal("58"), total=Decimal("928")),
    ]

    # Quote 4: Heizungstausch Becker (commercial, bigger) -- 5 items
    q4_items = [
        dict(quote_id=QUOTE_IDS[4], position=1, description="Demontage 2x Altkessel", category=LineCategory.labor, quantity=Decimal("10"), unit=Unit.hours, unit_price=Decimal("58"), total=Decimal("580")),
        dict(quote_id=QUOTE_IDS[4], position=2, description="Gas-Brennwertgerät 24kW (2x)", category=LineCategory.material, quantity=Decimal("2"), unit=Unit.pieces, unit_price=Decimal("3200"), total=Decimal("6400"), article_id=ART_GASBRENNWERT),
        dict(quote_id=QUOTE_IDS[4], position=3, description="Verrohrung und Hydraulik", category=LineCategory.material, quantity=Decimal("30"), unit=Unit.meters, unit_price=Decimal("12.80"), total=Decimal("384"), article_id=ART_KUPFERROHR_22),
        dict(quote_id=QUOTE_IDS[4], position=4, description="Regelungstechnik Kaskade", category=LineCategory.material, quantity=Decimal("1"), unit=Unit.pieces, unit_price=Decimal("890"), total=Decimal("890")),
        dict(quote_id=QUOTE_IDS[4], position=5, description="Installation und Inbetriebnahme", category=LineCategory.labor, quantity=Decimal("16"), unit=Unit.hours, unit_price=Decimal("58"), total=Decimal("928")),
    ]

    # Quote 5: Wärmepumpe Müller (active) -- 5 items
    q5_items = [
        dict(quote_id=QUOTE_IDS[5], position=1, description="Demontage Altgerät", category=LineCategory.labor, quantity=Decimal("8"), unit=Unit.hours, unit_price=Decimal("58"), total=Decimal("464")),
        dict(quote_id=QUOTE_IDS[5], position=2, description="Luft-Wasser-Wärmepumpe 8kW", category=LineCategory.material, quantity=Decimal("1"), unit=Unit.pieces, unit_price=Decimal("8500"), total=Decimal("8500"), article_id=ART_WAERMEPUMPE),
        dict(quote_id=QUOTE_IDS[5], position=3, description="Pufferspeicher 300L", category=LineCategory.material, quantity=Decimal("1"), unit=Unit.pieces, unit_price=Decimal("1200"), total=Decimal("1200")),
        dict(quote_id=QUOTE_IDS[5], position=4, description="Verrohrung und Elektrik", category=LineCategory.labor, quantity=Decimal("16"), unit=Unit.hours, unit_price=Decimal("58"), total=Decimal("928")),
        dict(quote_id=QUOTE_IDS[5], position=5, description="Inbetriebnahme und Einweisung", category=LineCategory.labor, quantity=Decimal("4"), unit=Unit.hours, unit_price=Decimal("62"), total=Decimal("248")),
    ]

    # Quote 6: Rohrbruch Fischer (active) -- 3 items
    q6_items = [
        dict(quote_id=QUOTE_IDS[6], position=1, description="Leckortung und Freilegung", category=LineCategory.labor, quantity=Decimal("3"), unit=Unit.hours, unit_price=Decimal("65"), total=Decimal("195")),
        dict(quote_id=QUOTE_IDS[6], position=2, description="Kupferrohr 15mm + Fittings", category=LineCategory.material, quantity=Decimal("5"), unit=Unit.meters, unit_price=Decimal("8.50"), total=Decimal("42.50"), article_id=ART_KUPFERROHR_15),
        dict(quote_id=QUOTE_IDS[6], position=3, description="Reparatur und Dichtprüfung", category=LineCategory.labor, quantity=Decimal("2"), unit=Unit.hours, unit_price=Decimal("65"), total=Decimal("130")),
    ]

    # Quote 7: Wartung Wagner (active/planned) -- 3 items
    q7_items = [
        dict(quote_id=QUOTE_IDS[7], position=1, description="Heizungswartung jährlich", category=LineCategory.labor, quantity=Decimal("2"), unit=Unit.hours, unit_price=Decimal("62"), total=Decimal("124")),
        dict(quote_id=QUOTE_IDS[7], position=2, description="Verschleißteile", category=LineCategory.material, quantity=Decimal("1"), unit=Unit.flat_rate, unit_price=Decimal("40"), total=Decimal("40")),
        dict(quote_id=QUOTE_IDS[7], position=3, description="Abgasmessung", category=LineCategory.labor, quantity=Decimal("0.5"), unit=Unit.hours, unit_price=Decimal("62"), total=Decimal("31")),
    ]

    all_items_groups = [q0_items, q1_items, q2_items, q3_items, q4_items, q5_items, q6_items, q7_items]
    qli_map = {}  # quote_id -> list of QuoteLineItem IDs (for linking project line items)

    for group in all_items_groups:
        ids_for_quote = []
        for item in group:
            lid = qli_id()
            ids_for_quote.append(lid)
            session.merge(QuoteLineItem(id=lid, **item))
        qli_map[group[0]["quote_id"]] = ids_for_quote

    # ============================================================
    # Projects (5 completed + 3 active)
    # ============================================================

    projects_data = [
        # 5 completed
        dict(id=PROJECT_IDS[0], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_MUELLER_ID,
             quote_id=QUOTE_IDS[0], job_type_id=JT_BADSANIERUNG_ID, assigned_to=GESELLE_HOFFMANN_ID,
             status=ProjectStatus.completed, planned_hours=Decimal("24"), actual_hours=Decimal("29"),
             planned_cost=Decimal("8200"), actual_cost=Decimal("9100"), margin_pct=Decimal("18"),
             started_at=ago(170), completed_at=ago(155), created_at=ago(175)),
        dict(id=PROJECT_IDS[1], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_SCHMIDT_ID,
             quote_id=QUOTE_IDS[1], job_type_id=JT_HEIZUNGSTAUSCH_ID, assigned_to=GESELLE_HOFFMANN_ID,
             status=ProjectStatus.completed, planned_hours=Decimal("18"), actual_hours=Decimal("19"),
             planned_cost=Decimal("12400"), actual_cost=Decimal("12800"), margin_pct=Decimal("23"),
             started_at=ago(140), completed_at=ago(128), created_at=ago(145)),
        dict(id=PROJECT_IDS[2], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_FISCHER_ID,
             quote_id=QUOTE_IDS[2], job_type_id=JT_WARTUNG_ID, assigned_to=MEISTER_WEBER_ID,
             status=ProjectStatus.completed, planned_hours=Decimal("3"), actual_hours=Decimal("2.5"),
             planned_cost=Decimal("450"), actual_cost=Decimal("410"), margin_pct=Decimal("38"),
             started_at=ago(115), completed_at=ago(115), created_at=ago(118)),
        dict(id=PROJECT_IDS[3], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_WAGNER_ID,
             quote_id=QUOTE_IDS[3], job_type_id=JT_BADSANIERUNG_ID, assigned_to=GESELLE_HOFFMANN_ID,
             status=ProjectStatus.completed, planned_hours=Decimal("42"), actual_hours=Decimal("52"),
             planned_cost=Decimal("11500"), actual_cost=Decimal("13200"), margin_pct=Decimal("15"),
             started_at=ago(80), completed_at=ago(55), created_at=ago(85)),
        dict(id=PROJECT_IDS[4], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_BECKER_ID,
             quote_id=QUOTE_IDS[4], job_type_id=JT_HEIZUNGSTAUSCH_ID, assigned_to=GESELLE_HOFFMANN_ID,
             status=ProjectStatus.completed, planned_hours=Decimal("26"), actual_hours=Decimal("28"),
             planned_cost=Decimal("15800"), actual_cost=Decimal("16200"), margin_pct=Decimal("22"),
             started_at=ago(50), completed_at=ago(35), created_at=ago(55)),
        # 3 active
        dict(id=PROJECT_IDS[5], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_MUELLER_ID,
             quote_id=QUOTE_IDS[5], job_type_id=JT_WAERMEPUMPE_ID, assigned_to=GESELLE_HOFFMANN_ID,
             status=ProjectStatus.active, planned_hours=Decimal("28"), actual_hours=None,
             planned_cost=Decimal("18500"), actual_cost=None, margin_pct=None,
             started_at=ago(20), completed_at=None, created_at=ago(25)),
        dict(id=PROJECT_IDS[6], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_FISCHER_ID,
             quote_id=QUOTE_IDS[6], job_type_id=JT_ROHRBRUCH_ID, assigned_to=MEISTER_WEBER_ID,
             status=ProjectStatus.active, planned_hours=Decimal("5"), actual_hours=None,
             planned_cost=Decimal("1200"), actual_cost=None, margin_pct=None,
             started_at=ago(10), completed_at=None, created_at=ago(14)),
        dict(id=PROJECT_IDS[7], firm_id=WEBER_FIRM_ID, customer_id=CUSTOMER_WAGNER_ID,
             quote_id=QUOTE_IDS[7], job_type_id=JT_WARTUNG_ID, assigned_to=None,
             status=ProjectStatus.planned, planned_hours=Decimal("2.5"), actual_hours=None,
             planned_cost=Decimal("380"), actual_cost=None, margin_pct=None,
             started_at=None, completed_at=None, created_at=ago(8)),
    ]
    for p_data in projects_data:
        session.merge(Project(**p_data))

    # ============================================================
    # Project Line Items (actuals for completed projects)
    # ============================================================

    pli_counter = 0
    def pli_id():
        nonlocal pli_counter
        pli_counter += 1
        return uuid.UUID(f"71000000-0000-0000-0000-{pli_counter:012d}")

    # Project 0 (Badsanierung Müller) -- actuals exceed quoted (hours +21%)
    p0_qli = qli_map[QUOTE_IDS[0]]
    p0_items = [
        dict(project_id=PROJECT_IDS[0], quote_line_id=p0_qli[0], description="Demontage alte Sanitärobjekte", category=LineCategory.labor, actual_quantity=Decimal("10"), actual_unit_price=Decimal("58"), actual_total=Decimal("580"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(155)),
        dict(project_id=PROJECT_IDS[0], quote_line_id=p0_qli[1], description="Waschtisch 60cm weiß", category=LineCategory.material, actual_quantity=Decimal("1"), actual_unit_price=Decimal("165"), actual_total=Decimal("165"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(155)),
        dict(project_id=PROJECT_IDS[0], quote_line_id=p0_qli[2], description="WC-Vorwandelement 112cm", category=LineCategory.material, actual_quantity=Decimal("1"), actual_unit_price=Decimal("195"), actual_total=Decimal("195"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(155)),
        dict(project_id=PROJECT_IDS[0], quote_line_id=p0_qli[3], description="Duscharmatur Unterputz Thermostat", category=LineCategory.material, actual_quantity=Decimal("1"), actual_unit_price=Decimal("258"), actual_total=Decimal("258"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(155)),
        dict(project_id=PROJECT_IDS[0], quote_line_id=p0_qli[4], description="Installation und Anschlussarbeiten", category=LineCategory.labor, actual_quantity=Decimal("19"), actual_unit_price=Decimal("58"), actual_total=Decimal("1102"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(155)),
    ]

    # Project 1 (Heizungstausch Schmidt) -- close to quote
    p1_qli = qli_map[QUOTE_IDS[1]]
    p1_items = [
        dict(project_id=PROJECT_IDS[1], quote_line_id=p1_qli[0], description="Demontage Altgerät", category=LineCategory.labor, actual_quantity=Decimal("7"), actual_unit_price=Decimal("58"), actual_total=Decimal("406"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(128)),
        dict(project_id=PROJECT_IDS[1], quote_line_id=p1_qli[1], description="Gas-Brennwertgerät 24kW", category=LineCategory.material, actual_quantity=Decimal("1"), actual_unit_price=Decimal("3250"), actual_total=Decimal("3250"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(128)),
        dict(project_id=PROJECT_IDS[1], quote_line_id=p1_qli[2], description="Kupferrohr 22mm", category=LineCategory.material, actual_quantity=Decimal("18"), actual_unit_price=Decimal("13.20"), actual_total=Decimal("237.60"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(128)),
        dict(project_id=PROJECT_IDS[1], quote_line_id=p1_qli[3], description="Umwälzpumpe", category=LineCategory.material, actual_quantity=Decimal("1"), actual_unit_price=Decimal("385"), actual_total=Decimal("385"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(128)),
        dict(project_id=PROJECT_IDS[1], quote_line_id=p1_qli[4], description="Ausdehnungsgefäß", category=LineCategory.material, actual_quantity=Decimal("1"), actual_unit_price=Decimal("125"), actual_total=Decimal("125"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(128)),
        dict(project_id=PROJECT_IDS[1], quote_line_id=p1_qli[5], description="Installation und IBN", category=LineCategory.labor, actual_quantity=Decimal("12"), actual_unit_price=Decimal("58"), actual_total=Decimal("696"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(128)),
    ]

    # Project 2 (Wartung Fischer) -- slightly under quoted
    p2_qli = qli_map[QUOTE_IDS[2]]
    p2_items = [
        dict(project_id=PROJECT_IDS[2], quote_line_id=p2_qli[0], description="Heizungswartung", category=LineCategory.labor, actual_quantity=Decimal("2"), actual_unit_price=Decimal("62"), actual_total=Decimal("124"), logged_by=MEISTER_WEBER_ID, logged_at=ago(115)),
        dict(project_id=PROJECT_IDS[2], quote_line_id=p2_qli[1], description="Verschleißteile", category=LineCategory.material, actual_quantity=Decimal("1"), actual_unit_price=Decimal("38"), actual_total=Decimal("38"), logged_by=MEISTER_WEBER_ID, logged_at=ago(115)),
        dict(project_id=PROJECT_IDS[2], quote_line_id=p2_qli[2], description="Abgasmessung", category=LineCategory.labor, actual_quantity=Decimal("0.5"), actual_unit_price=Decimal("62"), actual_total=Decimal("31"), logged_by=MEISTER_WEBER_ID, logged_at=ago(115)),
    ]

    # Project 3 (Badsanierung Wagner) -- BIG overrun: +24% hours, materials over too
    p3_qli = qli_map[QUOTE_IDS[3]]
    p3_items = [
        dict(project_id=PROJECT_IDS[3], quote_line_id=p3_qli[0], description="Komplettdemontage Altbad", category=LineCategory.labor, actual_quantity=Decimal("16"), actual_unit_price=Decimal("58"), actual_total=Decimal("928"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(55)),
        dict(project_id=PROJECT_IDS[3], quote_line_id=p3_qli[1], description="Sanitärobjekte komplett", category=LineCategory.material, actual_quantity=Decimal("1"), actual_unit_price=Decimal("3200"), actual_total=Decimal("3200"), notes="Kundin wollte höherwertiges WC", logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(55)),
        dict(project_id=PROJECT_IDS[3], quote_line_id=p3_qli[2], description="Fliesen und Abdichtung", category=LineCategory.material, actual_quantity=Decimal("22"), actual_unit_price=Decimal("92"), actual_total=Decimal("2024"), notes="Mehr Fläche als vermessen", logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(55)),
        dict(project_id=PROJECT_IDS[3], quote_line_id=p3_qli[3], description="Rohinstallation", category=LineCategory.labor, actual_quantity=Decimal("18"), actual_unit_price=Decimal("58"), actual_total=Decimal("1044"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(55)),
        dict(project_id=PROJECT_IDS[3], quote_line_id=p3_qli[4], description="Montage und Endanschluss", category=LineCategory.labor, actual_quantity=Decimal("18"), actual_unit_price=Decimal("58"), actual_total=Decimal("1044"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(55)),
    ]

    # Project 4 (Heizungstausch Becker) -- slight overrun
    p4_qli = qli_map[QUOTE_IDS[4]]
    p4_items = [
        dict(project_id=PROJECT_IDS[4], quote_line_id=p4_qli[0], description="Demontage 2x Altkessel", category=LineCategory.labor, actual_quantity=Decimal("11"), actual_unit_price=Decimal("58"), actual_total=Decimal("638"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(35)),
        dict(project_id=PROJECT_IDS[4], quote_line_id=p4_qli[1], description="Gas-Brennwertgerät 24kW (2x)", category=LineCategory.material, actual_quantity=Decimal("2"), actual_unit_price=Decimal("3280"), actual_total=Decimal("6560"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(35)),
        dict(project_id=PROJECT_IDS[4], quote_line_id=p4_qli[2], description="Verrohrung", category=LineCategory.material, actual_quantity=Decimal("35"), actual_unit_price=Decimal("13.20"), actual_total=Decimal("462"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(35)),
        dict(project_id=PROJECT_IDS[4], quote_line_id=p4_qli[3], description="Regelungstechnik", category=LineCategory.material, actual_quantity=Decimal("1"), actual_unit_price=Decimal("920"), actual_total=Decimal("920"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(35)),
        dict(project_id=PROJECT_IDS[4], quote_line_id=p4_qli[4], description="Installation und IBN", category=LineCategory.labor, actual_quantity=Decimal("17"), actual_unit_price=Decimal("58"), actual_total=Decimal("986"), logged_by=GESELLE_HOFFMANN_ID, logged_at=ago(35)),
    ]

    all_pli = p0_items + p1_items + p2_items + p3_items + p4_items
    for item in all_pli:
        session.merge(ProjectLineItem(id=pli_id(), **item))

    # ============================================================
    # Events (audit trail)
    # ============================================================

    evt_counter = 0
    def evt_id():
        nonlocal evt_counter
        evt_counter += 1
        return uuid.UUID(f"80000000-0000-0000-0000-{evt_counter:012d}")

    events = []

    # Quote created events
    for i, q in enumerate(quotes_data):
        events.append(Event(
            id=evt_id(), entity_type=EventEntityType.quote, entity_id=q["id"],
            event_type=EventType.created, actor_id=MEISTER_WEBER_ID,
            payload={"total_net": str(q["total_net"])}, created_at=q["created_at"],
        ))

    # Quote status changes (sent, accepted)
    for i, q in enumerate(quotes_data):
        if q.get("sent_at"):
            events.append(Event(
                id=evt_id(), entity_type=EventEntityType.quote, entity_id=q["id"],
                event_type=EventType.status_changed, actor_id=BUERO_YILMAZ_ID,
                payload={"status": {"old": "draft", "new": "sent"}}, created_at=q["sent_at"],
            ))
        if q.get("accepted_at"):
            events.append(Event(
                id=evt_id(), entity_type=EventEntityType.quote, entity_id=q["id"],
                event_type=EventType.status_changed, actor_id=BUERO_YILMAZ_ID,
                payload={"status": {"old": "sent", "new": "accepted"}}, created_at=q["accepted_at"],
            ))

    # One quote update event (price change) -- for audit trail demo
    events.append(Event(
        id=evt_id(), entity_type=EventEntityType.quote, entity_id=QUOTE_IDS[1],
        event_type=EventType.updated, actor_id=MEISTER_WEBER_ID,
        payload={"total_net": {"old": "11800", "new": "12400"}, "reason": "Materialkosten korrigiert"},
        created_at=ago(151),
    ))

    # Project status changes
    for i, p in enumerate(projects_data):
        events.append(Event(
            id=evt_id(), entity_type=EventEntityType.project, entity_id=p["id"],
            event_type=EventType.created, actor_id=MEISTER_WEBER_ID,
            payload={"status": p["status"].value}, created_at=p["created_at"],
        ))
        if p.get("started_at"):
            events.append(Event(
                id=evt_id(), entity_type=EventEntityType.project, entity_id=p["id"],
                event_type=EventType.status_changed, actor_id=MEISTER_WEBER_ID,
                payload={"status": {"old": "planned", "new": "active"}}, created_at=p["started_at"],
            ))
        if p.get("completed_at"):
            events.append(Event(
                id=evt_id(), entity_type=EventEntityType.project, entity_id=p["id"],
                event_type=EventType.status_changed, actor_id=MEISTER_WEBER_ID,
                payload={"status": {"old": "active", "new": "completed"}}, created_at=p["completed_at"],
            ))

    for e in events:
        session.merge(e)

    # ============================================================
    # FirmBenchmark (Weber firm -- 3 job types, 2 metrics each)
    # ============================================================

    fb_counter = 0
    def fb_id():
        nonlocal fb_counter
        fb_counter += 1
        return uuid.UUID(f"90000000-0000-0000-0000-{fb_counter:012d}")

    period_start = date(2025, 4, 1)
    period_end = date(2026, 4, 1)

    firm_benchmarks = [
        # Badsanierung -- Weber is slower: 14h vs platform 12h
        FirmBenchmark(id=fb_id(), firm_id=WEBER_FIRM_ID, job_type_id=JT_BADSANIERUNG_ID,
                      metric=CLMetric.duration_h, currency="EUR", period_start=period_start, period_end=period_end,
                      sample_size=2, p25=Decimal("12"), p50=Decimal("14"), p75=Decimal("16"), mean=Decimal("14")),
        FirmBenchmark(id=fb_id(), firm_id=WEBER_FIRM_ID, job_type_id=JT_BADSANIERUNG_ID,
                      metric=CLMetric.margin_pct, currency="EUR", period_start=period_start, period_end=period_end,
                      sample_size=2, p25=Decimal("15"), p50=Decimal("16.5"), p75=Decimal("18"), mean=Decimal("16.5")),
        # Heizungstausch -- on par
        FirmBenchmark(id=fb_id(), firm_id=WEBER_FIRM_ID, job_type_id=JT_HEIZUNGSTAUSCH_ID,
                      metric=CLMetric.duration_h, currency="EUR", period_start=period_start, period_end=period_end,
                      sample_size=2, p25=Decimal("17"), p50=Decimal("18"), p75=Decimal("19"), mean=Decimal("18")),
        FirmBenchmark(id=fb_id(), firm_id=WEBER_FIRM_ID, job_type_id=JT_HEIZUNGSTAUSCH_ID,
                      metric=CLMetric.margin_pct, currency="EUR", period_start=period_start, period_end=period_end,
                      sample_size=2, p25=Decimal("22"), p50=Decimal("22.5"), p75=Decimal("23"), mean=Decimal("22.5")),
        # Wartung -- good margins
        FirmBenchmark(id=fb_id(), firm_id=WEBER_FIRM_ID, job_type_id=JT_WARTUNG_ID,
                      metric=CLMetric.duration_h, currency="EUR", period_start=period_start, period_end=period_end,
                      sample_size=1, p25=None, p50=Decimal("2.5"), p75=None, mean=Decimal("2.5")),
        FirmBenchmark(id=fb_id(), firm_id=WEBER_FIRM_ID, job_type_id=JT_WARTUNG_ID,
                      metric=CLMetric.margin_pct, currency="EUR", period_start=period_start, period_end=period_end,
                      sample_size=1, p25=None, p50=Decimal("38"), p75=None, mean=Decimal("38")),
    ]
    for fb in firm_benchmarks:
        session.merge(fb)

    # ============================================================
    # CLBenchmark (platform-wide -- 5 job types, 2 metrics each)
    # ============================================================

    cl_counter = 0
    def cl_id():
        nonlocal cl_counter
        cl_counter += 1
        return uuid.UUID(f"a0000000-0000-0000-0000-{cl_counter:012d}")

    cl_benchmarks = [
        # Badsanierung
        CLBenchmark(id=cl_id(), job_type_id=JT_BADSANIERUNG_ID, segment=Segment.shk, region="Niedersachsen",
                    metric=CLMetric.duration_h, currency="EUR", period_start=period_start, period_end=period_end,
                    sample_size=518, p25=Decimal("10"), p50=Decimal("12"), p75=Decimal("16"), mean=Decimal("12.8")),
        CLBenchmark(id=cl_id(), job_type_id=JT_BADSANIERUNG_ID, segment=Segment.shk, region="Niedersachsen",
                    metric=CLMetric.margin_pct, currency="EUR", period_start=period_start, period_end=period_end,
                    sample_size=518, p25=Decimal("20"), p50=Decimal("26"), p75=Decimal("32"), mean=Decimal("25.5")),
        CLBenchmark(id=cl_id(), job_type_id=JT_BADSANIERUNG_ID, segment=Segment.shk, region="Niedersachsen",
                    metric=CLMetric.quote_total, currency="EUR", period_start=period_start, period_end=period_end,
                    sample_size=518, p25=Decimal("6500"), p50=Decimal("8500"), p75=Decimal("12000"), mean=Decimal("9200")),
        # Heizungstausch
        CLBenchmark(id=cl_id(), job_type_id=JT_HEIZUNGSTAUSCH_ID, segment=Segment.shk, region="Niedersachsen",
                    metric=CLMetric.duration_h, currency="EUR", period_start=period_start, period_end=period_end,
                    sample_size=342, p25=Decimal("14"), p50=Decimal("16"), p75=Decimal("20"), mean=Decimal("16.8")),
        CLBenchmark(id=cl_id(), job_type_id=JT_HEIZUNGSTAUSCH_ID, segment=Segment.shk, region="Niedersachsen",
                    metric=CLMetric.margin_pct, currency="EUR", period_start=period_start, period_end=period_end,
                    sample_size=342, p25=Decimal("18"), p50=Decimal("24"), p75=Decimal("28"), mean=Decimal("23.5")),
        CLBenchmark(id=cl_id(), job_type_id=JT_HEIZUNGSTAUSCH_ID, segment=Segment.shk, region="Niedersachsen",
                    metric=CLMetric.quote_total, currency="EUR", period_start=period_start, period_end=period_end,
                    sample_size=342, p25=Decimal("9800"), p50=Decimal("11800"), p75=Decimal("15000"), mean=Decimal("12100")),
        # Wartung
        CLBenchmark(id=cl_id(), job_type_id=JT_WARTUNG_ID, segment=Segment.shk, region="Niedersachsen",
                    metric=CLMetric.duration_h, currency="EUR", period_start=period_start, period_end=period_end,
                    sample_size=1240, p25=Decimal("2"), p50=Decimal("3"), p75=Decimal("4"), mean=Decimal("3.1")),
        CLBenchmark(id=cl_id(), job_type_id=JT_WARTUNG_ID, segment=Segment.shk, region="Niedersachsen",
                    metric=CLMetric.margin_pct, currency="EUR", period_start=period_start, period_end=period_end,
                    sample_size=1240, p25=Decimal("28"), p50=Decimal("35"), p75=Decimal("42"), mean=Decimal("34.5")),
        # Rohrbruch
        CLBenchmark(id=cl_id(), job_type_id=JT_ROHRBRUCH_ID, segment=Segment.shk, region="Niedersachsen",
                    metric=CLMetric.duration_h, currency="EUR", period_start=period_start, period_end=period_end,
                    sample_size=287, p25=Decimal("3"), p50=Decimal("5"), p75=Decimal("8"), mean=Decimal("5.4")),
        CLBenchmark(id=cl_id(), job_type_id=JT_ROHRBRUCH_ID, segment=Segment.shk, region="Niedersachsen",
                    metric=CLMetric.margin_pct, currency="EUR", period_start=period_start, period_end=period_end,
                    sample_size=287, p25=Decimal("24"), p50=Decimal("30"), p75=Decimal("38"), mean=Decimal("30.2")),
        # Wärmepumpe
        CLBenchmark(id=cl_id(), job_type_id=JT_WAERMEPUMPE_ID, segment=Segment.shk, region="Niedersachsen",
                    metric=CLMetric.duration_h, currency="EUR", period_start=period_start, period_end=period_end,
                    sample_size=156, p25=Decimal("20"), p50=Decimal("24"), p75=Decimal("32"), mean=Decimal("25.2")),
        CLBenchmark(id=cl_id(), job_type_id=JT_WAERMEPUMPE_ID, segment=Segment.shk, region="Niedersachsen",
                    metric=CLMetric.margin_pct, currency="EUR", period_start=period_start, period_end=period_end,
                    sample_size=156, p25=Decimal("16"), p50=Decimal("22"), p75=Decimal("26"), mean=Decimal("21.5")),
        CLBenchmark(id=cl_id(), job_type_id=JT_WAERMEPUMPE_ID, segment=Segment.shk, region="Niedersachsen",
                    metric=CLMetric.quote_total, currency="EUR", period_start=period_start, period_end=period_end,
                    sample_size=156, p25=Decimal("14000"), p50=Decimal("17200"), p75=Decimal("22000"), mean=Decimal("17800")),
    ]
    for cl in cl_benchmarks:
        session.merge(cl)

    # ============================================================
    # ArticlePriceHistory (copper pipe hero + 2 others)
    # ============================================================

    aph_counter = 0
    def aph_id():
        nonlocal aph_counter
        aph_counter += 1
        return uuid.UUID(f"b0000000-0000-0000-0000-{aph_counter:012d}")

    today = date(2026, 4, 13)

    # Kupferrohr 15mm -- upward trend (+8% over 30 days)
    copper_prices = [
        (today - timedelta(days=180), Decimal("7.20")),
        (today - timedelta(days=150), Decimal("7.35")),
        (today - timedelta(days=120), Decimal("7.50")),
        (today - timedelta(days=90), Decimal("7.65")),
        (today - timedelta(days=60), Decimal("7.85")),
        (today - timedelta(days=30), Decimal("7.90")),
        (today, Decimal("8.50")),
    ]
    for recorded, price in copper_prices:
        session.merge(ArticlePriceHistory(
            id=aph_id(), article_id=ART_KUPFERROHR_15, price=price,
            currency="EUR", source="DATANORM", recorded_at=recorded,
        ))

    # Gas-Brennwertgerät -- stable
    gas_prices = [
        (today - timedelta(days=180), Decimal("3150")),
        (today - timedelta(days=120), Decimal("3180")),
        (today - timedelta(days=60), Decimal("3200")),
        (today, Decimal("3200")),
    ]
    for recorded, price in gas_prices:
        session.merge(ArticlePriceHistory(
            id=aph_id(), article_id=ART_GASBRENNWERT, price=price,
            currency="EUR", source="Viessmann", recorded_at=recorded,
        ))

    # Wärmepumpe -- slight decrease
    wp_prices = [
        (today - timedelta(days=180), Decimal("9200")),
        (today - timedelta(days=120), Decimal("8900")),
        (today - timedelta(days=60), Decimal("8700")),
        (today, Decimal("8500")),
    ]
    for recorded, price in wp_prices:
        session.merge(ArticlePriceHistory(
            id=aph_id(), article_id=ART_WAERMEPUMPE, price=price,
            currency="EUR", source="Viessmann", recorded_at=recorded,
        ))

    session.commit()
    print(f"  Historical data seeded: 8 quotes, 8 projects, {len(all_pli)} project line items, {len(events)} events")
    print(f"  {len(firm_benchmarks)} firm benchmarks, {len(cl_benchmarks)} CL benchmarks, {len(copper_prices)+len(gas_prices)+len(wp_prices)} price history records")


def main():
    print("Seeding Workshop prototype database...")
    session = SessionLocal()
    try:
        seed_reference_data(session)
        seed_historical_data(session)
        print("Done!")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
