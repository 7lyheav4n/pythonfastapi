from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud, schemas

router = APIRouter(prefix="/factions", tags=["factions"])

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
    
# ------- GET -------------------------------------------------------
@router.get("", response_model=list[schemas.FactionResponse])
@router.get("/", response_model=list[schemas.FactionResponse])
def list_factions(db: Session = Depends(get_db)):
    return crud.get_factions(db)

@router.get("/affiliation/{affiliation}", response_model=list[schemas.FactionResponse])
def get_by_affiliation(affiliation: str, db: Session = Depends(get_db)):
    results = crud.get_factions_by_affiliation(db, affiliation)
    if not results:
        raise HTTPException(status_code=404, detail=f"No factions found for affiliation: {affiliation}")
    return results
 
@router.get("/{faction_id}", response_model=schemas.FactionResponse)
def get_faction(faction_id: str, db: Session = Depends(get_db)):
    faction = crud.get_faction_by_id(db, faction_id)
    if not faction:
        raise HTTPException(status_code=404, detail=f"Faction not found: {faction_id}")
    return faction


# ------- POST -------------------------------------------------------
@router.post("", response_model=schemas.FactionResponse)
@router.post("/", response_model=schemas.FactionResponse)
def create_faction(faction: schemas.FactionCreate, db: Session = Depends(get_db)):
    return crud.create_faction(db, faction)
 

# ------- Seed (JSON file → DB) ---------------------------------------------------
@router.post("/seed", summary="Seed all factions from JSON files")
def seed_factions(db: Session = Depends(get_db)):
    inserted = crud.seed_factions(db)
    if inserted:
        return {"message": "Seeded successfully", "inserted": inserted}
    return {"message": "All factions already exist, nothing inserted"}


