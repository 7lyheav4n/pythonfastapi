from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud, schemas

router = APIRouter(prefix="/units", tags=["units"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[schemas.UnitResponse])
@router.get("/", response_model=list[schemas.UnitResponse])
def list_units(db: Session = Depends(get_db)):
    return crud.get_units(db)

@router.post("", response_model=schemas.UnitResponse)
@router.post("/", response_model=schemas.UnitResponse)
def create_unit(unit: schemas.UnitCreate, db: Session = Depends(get_db)):
    return crud.create_unit(db, unit)

@router.get("/faction/{faction_name}", response_model=list[schemas.UnitResponse])
def get_by_faction(faction_name: str, db: Session = Depends(get_db)):
    units = crud.get_units_by_faction(db, faction_name)
    if not units:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"No units found for faction: {faction_name}")
    return units

@router.get("/factions", response_model=list[str])
def list_factions(db: Session = Depends(get_db)):
    return crud.get_all_factions(db)

# ------- Seed (JSON file → DB) -------------------------------------------------------
@router.post("/seed", summary="Seed units from seeds/units.json")
def seed_units(db: Session = Depends(get_db)):
    inserted = crud.seed_units(db)
    if inserted:
        return {"message": "Seeded successfully", "inserted": inserted}
    return {"message": "All units already exist, nothing inserted"}