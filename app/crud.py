from sqlalchemy.orm import Session
from . import models, schemas

FIXED_ITEMS = [
    {"name": "white_gold_grail", "class_name": "Holy",   "description": "Holy artifact — the sacred chalice said to grant eternal life to the mortal world."},
    {"name": "holy_jaw", "class_name": "Mythic", "description": "Mythic relic — the preserved teeth of Saint Anthony, believed to speak divine truth."},
    {"name": "enima", "class_name": "Legend", "description": "Legendary weapon — the Spear of Fate, true to behold decide the destiny of whoever it pierces."},
]

FIXED_UNITS = [
    {
        "name": "stigmatic_nun",
        "faction": "Trench_Pilgrims",
        "allegiance": "faithful",
        "type": "trooper",
        "description": "The Stigmatic Nuns are female warrior-nuns who worship the Third Meta-Christ, and cover themselves in blood and injuries to match his. They are masters of close-combat and melee, brandishing swords and pistols as they make their way through No Man's Land without fear. Even when injured, they grow stronger, suffering as their Lord once did.",
    },
    {
        "name": "castigator",
        "faction": "Trench_Pilgrims",
        "allegiance": "faithful",
        "type": "elite",
        "description": "Tasked with instilling the Fear of God in the troops, this orthodoxy officer keeps the soldiers on the path of righteousness and punishes those who transgress. They are protected by their unwavering faith as well as by the saints they revere.",
    },
    {
        "name": "sin_eater",
        "faction": "Heretic_Legion;court_of_the_Seven_Headed_Serpent;Cult_of_the_Black_Grail",
        "allegiance": "heretic",
        "type": "mercenary",
        "description": "Sin Eaters are horrific creatures: once they were mortal men and women, but their overwhelming greed and hunger for human flesh tainted with Sin, combined with the corrupting influence of the Hellgate, has turned them into a form that matches their inner foulness.",
    },
]

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

def create_unit(db: Session, unit: schemas.UnitCreate):
    db_unit = models.Unit(**unit.model_dump())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

def get_units(db: Session):
    return db.query(models.Unit).all()