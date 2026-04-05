from sqlalchemy import Column, Integer, String
from .database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    faction = Column(String, nullable=False)
    allegiance = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=True)

class Currency(Base):
    __tablename__ = "currency"
    
    id = Column(Integer, primary_key=True, index=True)
    coinage = Column(String, nullable=False, unique=True)
    usage = Column(String, nullable=False)
    description = Column(String, nullable=True)