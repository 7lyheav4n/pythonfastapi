from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..modules.search import search_by_name


router = APIRouter(prefix="/search", tags=["search"])

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
    
@router.get("")
@router.get("/")
def search(q: str = Query(..., description="Name to search for"), db: Session = Depends(get_db)):
  return search_by_name(db, q)

