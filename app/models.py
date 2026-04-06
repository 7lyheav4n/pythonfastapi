from sqlalchemy import Column, Integer, String, UniqueConstraint
from .database import Base

# --------- items tables ---------------------------------------------

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

# ---------  currency tables ---------------------------------------------

class Currency(Base):
    __tablename__ = "currency"
    
    id = Column(Integer, primary_key=True, index=True)
    coinage = Column(String, nullable=False, unique=True)
    usage = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    
    
# --------- Faction unit tables ---------------------------------------------
 
class UnitCourtOfSevenHeaded(Base):
    __tablename__ = "units_court_of_seven_headed"
 
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    faction     = Column(String, nullable=False)
    allegiance  = Column(String, nullable=False)
    type        = Column(String, nullable=False)
    description = Column(String, nullable=True)
    __table_args__ = (UniqueConstraint("name", "faction", name="uq_court_name_faction"),)
 
 
class UnitCultOfBlackGrail(Base):
    __tablename__ = "units_cult_of_black_grail"
 
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    faction     = Column(String, nullable=False)
    allegiance  = Column(String, nullable=False)
    type        = Column(String, nullable=False)
    description = Column(String, nullable=True)
    __table_args__ = (UniqueConstraint("name", "faction", name="uq_cult_name_faction"),)
 
 
class UnitHereticLegion(Base):
    __tablename__ = "units_heretic_legion"
 
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    faction     = Column(String, nullable=False)
    allegiance  = Column(String, nullable=False)
    type        = Column(String, nullable=False)
    description = Column(String, nullable=True)
    __table_args__ = (UniqueConstraint("name", "faction", name="uq_heretic_name_faction"),)
 
 
class UnitNewAntioch(Base):
    __tablename__ = "units_new_antioch"
 
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    faction     = Column(String, nullable=False)
    allegiance  = Column(String, nullable=False)
    type        = Column(String, nullable=False)
    description = Column(String, nullable=True)
    __table_args__ = (UniqueConstraint("name", "faction", name="uq_new_antioch_name_faction"),)
 
 
class UnitTrenchPilgrims(Base):
    __tablename__ = "units_trench_pilgrims"
 
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    faction     = Column(String, nullable=False)
    allegiance  = Column(String, nullable=False)
    type        = Column(String, nullable=False)
    description = Column(String, nullable=True)
    __table_args__ = (UniqueConstraint("name", "faction", name="uq_trench_name_faction"),)
 
 
class UnitIronSultanate(Base):
    __tablename__ = "units_iron_sultanate"
 
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    faction     = Column(String, nullable=False)
    allegiance  = Column(String, nullable=False)
    type        = Column(String, nullable=False)
    description = Column(String, nullable=True)
    __table_args__ = (UniqueConstraint("name", "faction", name="uq_sultanate_name_faction"),)