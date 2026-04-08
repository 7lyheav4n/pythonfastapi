from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import Base, engine, SessionLocal
from .routers import items, currency, search, units, factions
from .routers.unit_router_factory import make_unit_router
from . import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="New Antioch API", redirect_slashes=False)

app.mount("/static", StaticFiles(directory="static"), name="static")


# --- START UP SEEDING -----------------------------------------------------------------------
@app.on_event("startup")
def startup_seed():
    db = SessionLocal()
    try:
        crud.seed_items(db)
        crud.seed_currency(db)
        crud.seed_units_new_antioch(db)
        crud.seed_units_trench_pilgrims(db)
        crud.seed_units_iron_sultanate(db)
        crud.seed_units_heretic(db)
        crud.seed_units_court(db)
        crud.seed_units_cult(db)
        crud.seed_factions(db)
        print("[startup] seed complete")
    finally:
        db.close()

# --- STATIC ROUTE -----------------------------------------------------------------------
@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/status")
def status():
    return {"message": "_New_Antioch_", "status": "online"}

# --- ROUTES -----------------------------------------------------------------------
app.include_router(items.router)
app.include_router(currency.router)
app.include_router(search.router)
app.include_router(units.router)
app.include_router(factions.router)

# --- FACTION's UNITS ROUTES -----------------------------------------------------------------------
app.include_router(make_unit_router(
    prefix="/units/court_of_seven_headed",
    tag="court of the seven headed serpent",
    get_all=crud.get_units_court,
    create=crud.create_unit_court,
    
    seed_fn=crud.seed_units_court,
))
 
app.include_router(make_unit_router(
    prefix="/units/cult_of_black_grail",
    tag="cult of the black grail",
    get_all=crud.get_units_cult,
    create=crud.create_unit_cult,
    
    seed_fn=crud.seed_units_cult,
))
 
app.include_router(make_unit_router(
    prefix="/units/heretic_legion",
    tag="heretic legion",
    get_all=crud.get_units_heretic,
    create=crud.create_unit_heretic,
    
    seed_fn=crud.seed_units_heretic,
))
 
app.include_router(make_unit_router(
    prefix="/units/new_antioch",
    tag="principality of new antioch",
    get_all=crud.get_units_new_antioch,
    create=crud.create_unit_new_antioch,
    
    seed_fn=crud.seed_units_new_antioch,
))
 
app.include_router(make_unit_router(
    prefix="/units/trench_pilgrims",
    tag="trench pilgrims",
    get_all=crud.get_units_trench,
    create=crud.create_unit_trench,
    
    seed_fn=crud.seed_units_trench_pilgrims,
))
 
app.include_router(make_unit_router(
    prefix="/units/iron_sultanate",
    tag="iron sultanate",
    get_all=crud.get_units_sultanate,
    create=crud.create_unit_sultanate,
    
    seed_fn=crud.seed_units_iron_sultanate,
))


