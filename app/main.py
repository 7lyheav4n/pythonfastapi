from fastapi import FastAPI
from .database import Base, engine
from .routers import items

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + PostgreSQL")

app.include_router(items.router)
