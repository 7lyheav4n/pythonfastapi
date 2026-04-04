import os
import json
from sqlalchemy.orm import Session
from . import models, schemas


SEEDS_DIR = os.path.join(os.path.dirname(__file__), "..", "seeds")

def load_seed(filename: str) -> list:
    path = os.path.join(SEEDS_DIR, filename)
    if not os.path.exists(path):
        print(f"[seed] file not found: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
# --------------------------------------------------------------------------------


# --------------------------------------------------------------------------------
def seed_items(db: Session):
    inserted = []
    for data in FIXED_ITEMS:
        exists = db.query(models.Item).filter(models.Item.name == data["name"]).first()
        if not exists:
            item = models.Item(**data)
            db.add(item)
            inserted.append(data["name"])
    db.commit()
    return inserted

def seed_units(db: Session):
    inserted = []
    for data in FIXED_UNITS:
        exists = db.query(models.Unit).filter(models.Unit.name == data["name"]).first()
        if not exists:
            db.add(models.Unit(**data))
            inserted.append(data["name"])
    db.commit()
    return inserted

def seed_currency(db: Session):
    inserted = []
    for data in FIXED_CURRENCY:
        exists = db.query(models.Currency).filter(models.Currency.coinage == data["coinage"]).first()
        if not exists:
            db.add(models.Currency(**data))
            inserted.append(data["coinage"])
    db.commit()
    return inserted

# --------------------------------------------------------------------------------
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
# --------------------------------------------------------------------------------
def create_unit(db: Session, unit: schemas.UnitCreate):
    db_unit = models.Unit(**unit.model_dump())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

def get_units(db: Session):
    return db.query(models.Unit).all()

def get_units_by_faction(db: Session, faction: str):
    return db.query(models.Unit).filter(
        models.Unit.faction.ilike(f"%{faction}%")
    ).all()
    
def get_all_factions(db: Session):
    rows = db.query(models.Unit.faction).distinct().all()
    factions = set()
    for row in rows:
        for f in row[0].split(";"):
            factions.add(f.strip())
    return sorted(factions)
# --------------------------------------------------------------------------------

def create_currency(db: Session, currency: schemas.CurrencyCreate):
    db_currency = models.Currency(**currency.model_dump())
    db.add(db_currency)
    db.commit()
    db.refresh(db_currency)
    return db_currency

def get_currencies(db: Session):
    return db.query(models.Currency).all()
    


