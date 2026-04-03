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