import os
import json
from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas


SEEDS_DIR = os.path.join(os.path.dirname(__file__), "..", "seeds")
# SEED LOADER
def load_seed(filename: str) -> list:
    path = os.path.join(SEEDS_DIR, filename)
    if not os.path.exists(path):
        print(f"[seed] file not found: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)



# --- Generic unit seed helper -------------------------------------------------------
def _seed_unit_table(db: Session, model, filename: str) -> list:
    inserted = []
    for data in load_seed(filename):
        exists = db.query(model).filter(
            model.name == data["name"],
            model.faction == data["faction"],
        ).first()
        if not exists:
            db.add(model(**data))
            inserted.append(data["name"])
    db.commit()
    return inserted



# -------------------- SEEDING FUNCTIONS -------------------------------------------------------
def seed_items(db: Session):
    inserted = []
    for data in load_seed("items.json"):
        exists = db.query(models.Item).filter(models.Item.name == data["name"]).first()
        if not exists:
            db.add(models.Item(**data))
            inserted.append(data["name"])
    db.commit()
    return inserted

def seed_currency(db: Session):
    inserted = []
    for data in load_seed("currency.json"):
        exists = db.query(models.Currency).filter(models.Currency.coinage == data["coinage"]).first()
        if not exists:
            db.add(models.Currency(**data))
            inserted.append(data["coinage"])
    db.commit()
    return inserted

def seed_units_court(db: Session):
    return _seed_unit_table(db, models.UnitCourtOfSevenHeaded, "court_of_seven-headed_units.json")
 
def seed_units_cult(db: Session):
    return _seed_unit_table(db, models.UnitCultOfBlackGrail, "cult_of_black_grail_units.json")
 
def seed_units_heretic(db: Session):
    return _seed_unit_table(db, models.UnitHereticLegion, "heretic_legion_units.json")
 
def seed_units_new_antioch(db: Session):
    return _seed_unit_table(db, models.UnitNewAntioch, "new_antioch_units.json")
 
def seed_units_trench_pilgrims(db: Session):
    return _seed_unit_table(db, models.UnitTrenchPilgrims, "trench_pilgrim_units.json")
 
def seed_units_iron_sultanate(db: Session):
    return _seed_unit_table(db, models.UnitIronSultanate, "iron_sultanate_units.json")


# --- Generic unit CRUD helper -------------------------------------------------------
def _get_units(db: Session, model):
    return db.query(model).all()
 
def _create_unit(db: Session, model, unit: schemas.UnitCreate):
    db_unit = model(**unit.model_dump())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit
 
def _get_units_by_faction(db: Session, model, factions: list[str]):
    filters = [model.faction.ilike(f"%{f}%") for f in factions]
    return db.query(model).filter(or_(*filters)).all()
 
def _get_all_factions(db: Session, model):
    rows = db.query(model.faction).distinct().all()
    factions = set()
    for row in rows:
        for f in row[0].split(";"):
            factions.add(f.strip())
    return sorted(factions)
 
## --- GET ALL UNITS -----------------------------------------------

def get_all_units(db: Session) -> dict:
    return {
        "court_of_seven_headed": _get_units(db, models.UnitCourtOfSevenHeaded),
        "cult_of_black_grail":   _get_units(db, models.UnitCultOfBlackGrail),
        "heretic_legion":        _get_units(db, models.UnitHereticLegion),
        "new_antioch":           _get_units(db, models.UnitNewAntioch),
        "trench_pilgrims":       _get_units(db, models.UnitTrenchPilgrims),
        "iron_sultanate":        _get_units(db, models.UnitIronSultanate),
    }

    
# --- Court of the Seven Headed Serpent -----------------------------------------------
 
def get_units_court(db: Session):
    return _get_units(db, models.UnitCourtOfSevenHeaded)
 
def create_unit_court(db: Session, unit: schemas.UnitCreate):
    return _create_unit(db, models.UnitCourtOfSevenHeaded, unit)
 
 
 
# --- Cult of the Black Grail -----------------------------------------------------------
 
def get_units_cult(db: Session):
    return _get_units(db, models.UnitCultOfBlackGrail)
 
def create_unit_cult(db: Session, unit: schemas.UnitCreate):
    return _create_unit(db, models.UnitCultOfBlackGrail, unit)
 
 
 
# --- Heretic Legion ------------------------------------------------------------------
 
def get_units_heretic(db: Session):
    return _get_units(db, models.UnitHereticLegion)
 
def create_unit_heretic(db: Session, unit: schemas.UnitCreate):
    return _create_unit(db, models.UnitHereticLegion, unit)
 

 
# --- New Antioch -----------------------------------------------------------------
 
def get_units_new_antioch(db: Session):
    return _get_units(db, models.UnitNewAntioch)
 
def create_unit_new_antioch(db: Session, unit: schemas.UnitCreate):
    return _create_unit(db, models.UnitNewAntioch, unit)
 

 
 
# --- Trench Pilgrims ---------------------------------------------------------------
 
def get_units_trench(db: Session):
    return _get_units(db, models.UnitTrenchPilgrims)
 
def create_unit_trench(db: Session, unit: schemas.UnitCreate):
    return _create_unit(db, models.UnitTrenchPilgrims, unit)
 

 
 
# --- Iron Sultanate -------------------------------------------------------------
def get_units_sultanate(db: Session):
    return _get_units(db, models.UnitIronSultanate)
 
def create_unit_sultanate(db: Session, unit: schemas.UnitCreate):
    return _create_unit(db, models.UnitIronSultanate, unit)
 


# ------------------ ITEM CRUD -------------------------------------------------------
def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session):
    items = db.query(models.Item).all()
    print(f"[DEBUG] items found: {len(items)}")  # ← add this
    for i in items:
        print(f"  -> {i.id} {i.name}")
    return items




# --------------------- CURRENCY CRUD -----------------------------------------------
def create_currency(db: Session, currency: schemas.CurrencyCreate):
    db_currency = models.Currency(**currency.model_dump())
    db.add(db_currency)
    db.commit()
    db.refresh(db_currency)
    return db_currency

def get_currencies(db: Session):
    return db.query(models.Currency).all()





