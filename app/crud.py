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
    return _seed_unit_table(db, models.UnitCourtOfSevenHeaded, "units/court_of_seven-headed_units.json")
 
def seed_units_cult(db: Session):
    return _seed_unit_table(db, models.UnitCultOfBlackGrail, "units/cult_of_black_grail_units.json")
 
def seed_units_heretic(db: Session):
    return _seed_unit_table(db, models.UnitHereticLegion, "units/heretic_legion_units.json")
 
def seed_units_new_antioch(db: Session):
    return _seed_unit_table(db, models.UnitNewAntioch, "units/new_antioch_units.json")
 
def seed_units_trench_pilgrims(db: Session):
    return _seed_unit_table(db, models.UnitTrenchPilgrims, "units/trench_pilgrim_units.json")
 
def seed_units_iron_sultanate(db: Session):
    return _seed_unit_table(db, models.UnitIronSultanate, "units/iron_sultanate_units.json")


# --- Generic unit CRUD helper -------------------------------------------------------
def _get_units(db: Session, model):
    return db.query(model).all()
 
def _create_unit(db: Session, model, unit: schemas.UnitCreate):
    db_unit = model(**unit.model_dump())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit
 

 
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


# --------------------- FACTION CRUD -----------------------------------------------

# _LORE_KEYS_ = {
#     "fortifications", "sub_forces", # new anitoch (assets,  allies)
#     "the_iron_wall", "takwin", # iron sultanate (assets, allies)
#     "processions",             # trench pilgrims (assets)
#     "countermeasures",         # cult of black grail (against)
#     "goetic_powers"            # court of seven headed (attack)
# }

_LORE_KEYS = {
    "the_iron_wall", "takwin",           # iron sultanate
    "fortifications",                    # new antioch
    "goetic_powers",                     # court of seven headed
    "countermeasures",                   # cult of black grail
}

def _parse_faction(data: dict) -> dict:
    lore = {k: data.pop(k) for k in list(data.keys()) if k in _LORE_KEYS}
    # normalise sub_factions key — json files use sub_factions / sub_forces / processions
    for key in ("sub_forces", "processions"):
        if key in data:
            data["sub_factions"] = data.pop(key)
    if lore:
        data["lore"] = lore
    return data
 
def seed_factions(db: Session):
    files = [
        "lore/faction_iron_sultanate.json",
        "lore/faction_principality_of_new_antioch.json",
        "lore/faction_trench_pilgrims.json",
        "lore/faction_court_of_the_seven_headed_serpent.json",
        "lore/faction_cult_of_the_black_grail.json",
        "lore/faction_heretic_legion.json"
    ]
    inserted = []
    for filename in files:
        raw = load_seed(filename)
        if not raw:
            continue
        data = _parse_faction(dict(raw))
        exists = db.query(models.Factions).filter(models.Factions.id == data["id"]).first()
        if not exists:
            db.add(models.Factions(**data))
            inserted.append(data["id"])
    db.commit()
    return inserted
 
def get_factions(db: Session):
    return db.query(models.Factions).all()
 
def get_faction_by_id(db: Session, faction_id: str):
    return db.query(models.Factions).filter(models.Factions.id == faction_id).first()
 
def get_factions_by_affiliation(db: Session, affiliation: str):
    return db.query(models.Factions).filter(
        models.Factions.affiliation.ilike(f"%{affiliation}%")
    ).all()
 
def create_faction(db: Session, faction: schemas.FactionCreate):
    data = _parse_faction(dict(faction.model_dump()))
    db_faction = models.Factions(**data)
    db.add(db_faction)
    db.commit()
    db.refresh(db_faction)
    return db_faction