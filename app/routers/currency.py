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
def list_currency(db: Session = Depends(get_db)):
    return crud.get_currency(db)

@router.post("", response_model=schemas.CurrencyResponse)
@router.post("/", response_model=schemas.CurrencyResponse)
def create_currency(unit: schemas.CurrencyCreate, db: Session = Depends(get_db)):
    return crud.create_currency(db, unit)