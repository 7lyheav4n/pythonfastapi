from fastapi import FastAPI
from .database import Base, engine, SessionLocal
from .routers import items
from . import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + PostgreSQL", redirect_slashes=False)

app.include_router(items.router)

@app.on_event("startup")
def startup_seed():
    db = SessionLocal()
    try:
        crud.seed_items(db)
        print("[startup] seed complete")
    finally:
        db.close()