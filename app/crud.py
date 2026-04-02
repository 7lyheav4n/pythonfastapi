from sqlalchemy.orm import Session
from . import models, schemas

FIXED_ITEMS = [
    {"id": 1, "name": "white_gold_grail", "class_name": "Holy",   "description": "Holy artifact — the sacred chalice said to grant eternal life to the mortal world."},
    {"id": 2, "name": "holy_jaw",         "class_name": "Mythic", "description": "Mythic relic — the preserved teeth of Saint Anthony, believed to speak divine truth."},
    {"id": 3, "name": "enima",            "class_name": "Legend", "description": "Legendary weapon — the Spear of Fate, true to behold decide the destiny of whoever it pierces."},
]

def seed_items(db: Session):
    inserted = []
    for data in FIXED_ITEMS:
        exists = db.query(models.Item).filter(models.Item.id == data["id"]).first()
        if not exists:
            item = models.Item(**data)
            db.add(item)
            inserted.append(data["name"])
    db.commit()
    return inserted

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