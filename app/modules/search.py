import time
from sqlalchemy.orm import Session
from app import models


def _serialize(obj) -> dict:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


def _search_model(db: Session, model, field) -> tuple[list, float]:
    t0 = time.perf_counter()
    rows = db.query(model).filter(field.ilike(f"%{query}%")).all()
    ms = (time.perf_counter() - t0) * 1000
    return rows, ms


def search_by_name(db: Session, query: str) -> dict:
    searches = [
        ("items",      models.Item,     models.Item.name),
        ("currencies", models.Currency, models.Currency.coinage),
        ("new_antioch", models.UnitNewAntioch, models.UnitNewAntioch.name),
        ("iron_sultanate", models.UnitIronSultanate, models.UnitIronSultanate.name),
        ("trench_pilgrims", models.UnitTrenchPilgrims, models.UnitTrenchPilgrims.name),
        ("heretic_legion", models.UnitHereticLegion, models.UnitHereticLegion.name),
        ("court_of_seven_headed", models.UnitCourtOfSevenHeaded, models.UnitCourtOfSevenHeaded.name),
        ("cult_of_black_grail", models.UnitCultOfBlackGrail, models.UnitCultOfBlackGrail.name)
    ]

    timing = {}
    results = {}
    total = 0

    for label, model, field in searches:
        t0 = time.perf_counter()
        rows = db.query(model).filter(field.ilike(f"%{query}%")).all()
        ms = round((time.perf_counter() - t0) * 1000, 3)

        timing[f"{label}_ms"] = ms
        results[label] = [_serialize(row) for row in rows]
        total += len(rows)

        print(f"[search] {label:<12} → {len(rows)} result(s) in {ms:.3f}ms")

    total_ms = round(sum(timing.values()), 3)
    timing["total_ms"] = total_ms
    print(f"[search] total        → {total} result(s) in {total_ms:.3f}ms combined")

    return {
        "query":       query,
        "total_found": total,
        "timing":      timing,
        "results":     results,
    }