from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Callable, List
from ..database import SessionLocal
from .. import schemas


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def make_unit_router(
    prefix: str,
    tag: str,
    get_all: Callable,
    create: Callable,
    by_faction: Callable,
    get_factions: Callable,
    seed_fn: Callable,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[tag])

    @router.get("", response_model=list[schemas.UnitResponse])
    @router.get("/", response_model=list[schemas.UnitResponse])
    def list_units(db: Session = Depends(get_db)):
        return get_all(db)

    @router.get("/factions", response_model=list[str])
    def list_factions(db: Session = Depends(get_db)):
        return get_factions(db)

    @router.get("/faction", response_model=list[schemas.UnitResponse])
    def get_by_faction(
        faction_name: List[str] = Query(..., description="One or more faction names"),
        db: Session = Depends(get_db),
    ):
        units = by_faction(db, faction_name)
        if not units:
            raise HTTPException(status_code=404, detail=f"No units found for: {faction_name}")
        return units

    @router.post("", response_model=schemas.UnitResponse)
    @router.post("/", response_model=schemas.UnitResponse)
    def create_unit(unit: schemas.UnitCreate, db: Session = Depends(get_db)):
        return create(db, unit)

    @router.post("/seed", summary=f"Seed {tag} from JSON file")
    def seed_units(db: Session = Depends(get_db)):
        inserted = seed_fn(db)
        if inserted:
            return {"message": "Seeded successfully", "inserted": inserted}
        return {"message": "All units already exist, nothing inserted"}

    return router