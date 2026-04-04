from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud, schemas

router = APIRouter(prefix="/currency", tags=["currency"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[schemas.CurrencyResponse])
@router.get("/", response_model=list[schemas.CurrencyResponse])
def list_currencies(db: Session = Depends(get_db)):
    return crud.get_currencies(db)

@router.post("", response_model=schemas.CurrencyResponse)
@router.post("/", response_model=schemas.CurrencyResponse)
def create_currency(currency: schemas.CurrencyCreate, db: Session = Depends(get_db)):
    return crud.create_currency(db, currency)


# ------- Seed (JSON file → DB) -------------------------------------------------------
@router.post("/seed", summary="Seed currency from seeds/currency.json")
def seed_currency(db: Session = Depends(get_db)):
    inserted = crud.seed_currency(db)
    if inserted:
        return {"message": "Seeded successfully", "inserted": inserted}
    return {"message": "All currencies already exist, nothing inserted"}