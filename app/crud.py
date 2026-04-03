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

FIXED_CURRENCY = [
    {
        "coinage": "ducat",
        "usage": "principality_of_new_antioch",
        "description": "The Currency of the city of The Principality of New Antioch is the Ducat, used throughout the Levant by Faithful forces to buy weapons, equipment, and recruit mercenaries."
    },
    {
        "coinage": "dinar",
        "usage": "sultanate_of_the_iron_wall",
        "description": "The rich mines within the Great Iron wall produce gold aplenty, and the Sultanate issues gold dinars and silver drachms with exceeding purity and standardised weight. The coins are produced by the alchemists of the House of Wisdom, which explains their extraordinary craftsmanship and artistry. The law severely punishes those who try to debase dinars by being hung and disemboweled simultaneously."
    },
    {
        "coinage": "silver_coin",
        "usage": "heretic_legionaire",
        "description": "heretic nations also value coin, for avarice of Mammon, one of the great princes of Hell knows no bounds, and he controls the commerce in the domains of the damned. Mammon’s greed is such that most gold ends up in his coffers in the Fourth Circle of Hell, but just enough silver remains in calculation as to form the most common coinage. These coins come with various symbols of rival Arch-devils, but they all have blasphemous text extolling the betrayal of the redeemer by Judas. Each piece of silver is tarnished due the taint of Hell."
    },
    {
        "coinage": "souls",
        "usage": "cult_of_the_Black_Grail;court_of_the_seven_headed_serpent",
        "description": "bodies of men, horses, dogs, insects and other animals of every kind that are infected by the Black Grail lurch to their feet, driven by a demonic will. Not living, not dead, they become vessels to spread the corruption of their master ever further, forming warbands that strive to find and infect life of any kind."
    },
    {
        "coinage": "slaves",
        "usage": "court_of_the_seven_headed_serpent",
        "description": "living human slave soldiers of the Court known as the wretched. These unfortunate souls possess not a drop of demon blood. They act as disposable shock troops or are used as subjects of torture to power the Goetic magic of the sorcerers and other users of the dark arts."
    }
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

def seed_currency(db: Session):
    inserted = []
    for data in FIXED_CURRENCY:
        exists = db.query(models.Currency).filter(models.Currency.coinage == data["coinage"]).first()
        if not exists:
            db.add(models.Currency(**data))
            inserted.append(data["coinage"])
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

def create_currency(db: Session, currency: schemas.CurrencyCreate):
    db_currency = models.Currency(**currency.model_dump())
    db.add(db_currency)
    db.commit()
    db.refresh(db_currency)
    return db_currency

def get_currencies(db: Session):
    return db.query(models.Currency).all()
    
    