from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Callable, List
from ..database import SessionLocal
from .. import schemas


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def make_unit_router(
    prefix: str,
    tag: str,
    get_all: Callable,
    create: Callable,
    seed_fn: Callable,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[tag])

    @router.get("", response_model=list[schemas.UnitResponse])
    @router.get("/", response_model=list[schemas.UnitResponse])
    def list_units(db: Session = Depends(get_db)):
        return get_all(db)


    @router.post("", response_model=schemas.UnitResponse)
    @router.post("/", response_model=schemas.UnitResponse)
    def create_unit(unit: schemas.UnitCreate, db: Session = Depends(get_db)):
        return create(db, unit)

    return router