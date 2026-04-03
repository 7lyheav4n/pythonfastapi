from email import message
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import Base, engine, SessionLocal
from .routers import items, units, currency
from . import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + PostgreSQL", redirect_slashes=False)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(items.router)
app.include_router(units.router)
app.include_router(currency.router)

@app.on_event("startup")
def startup_seed():
    db = SessionLocal()
    try:
        crud.seed_items(db)
        crud.seed_units(db)
        crud.seed_currency(db)
        print("[startup] seed complete")
    finally:
        db.close()
        
@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/status")
def status():
    return {"message": "_New_Antioch_", "status": "online"}