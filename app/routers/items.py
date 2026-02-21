from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud, schemas

router = APIRouter(prefix="/items", tags=["items"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@router.get("/", response_model=list[schemas.ItemResponse])
def list_items(db: Session = Depends(get_db)):
    return crud.get_items(db)
