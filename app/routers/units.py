from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud

router = APIRouter(prefix="/units", tags=["units"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
@router.get("/")
def list_all_units(db: Session = Depends(get_db)):
    return crud.get_all_units(db)