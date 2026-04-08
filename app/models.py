from operator import index
from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .database import Base

# --------- items tables ---------------------------------------------

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)


    
# --------- Factions table ---------------------------------------------
class Factions(Base):
    __tablename__ = "factions"
    
    id          = Column(String, primary_key=True) # "iron_sultanate" from JSON id field
    name        = Column(String, nullable=False)
    full_name   = Column(String, nullable=True)    # only some factions have this
    affiliation = Column(String, nullable=False)   # must be "faithful" or "heretic"
    religion    = Column(String, nullable=True)
    capital     = Column(String, nullable=True)
    language    = Column(JSONB,  nullable=True)    # array of strings
    currency    = Column(String, nullable=True)
    description = Column(String, nullable=True)
    government  = Column(JSONB,  nullable=True)    # nested object varies per faction
    sub_factions= Column(JSONB,  nullable=True)    # sub_factions; sub_forces; processions
    units       = Column(JSONB,  nullable=True)    # {elites: [], troops: [], mercenaries: []}
    lore        = Column(JSONB,  nullable=True)    # catch-all for unique per-faction fields
    
# --------- Tables Relationship ORM ---------------------------------------------
currency            = relationship("Currency",              back_populates="faction_rel")
units_court         = relationship("UnitCourtOfSevenHeaded",back_populates="faction_rel")
units_cult          = relationship("UnitCultOfBlackGrail",  back_populates="faction_rel")
units_heretic       = relationship("UnitHereticLegion",     back_populates="faction_rel")
units_new_antioch   = relationship("UnitNewAntioch",        back_populates="faction_rel")
units_pilgrims      = relationship("UnitTrenchPilgrims",    back_populates="faction_rel")
units_sultanate     = relationship("UnitIronSultanate",     back_populates="faction_rel")



# ---------  currency tables ---------------------------------------------
class Currency(Base):
    __tablename__ = "currency"
    
    id          = Column(Integer, primary_key=True, index=True)
    coinage     = Column(String, nullable=False, unique=True)
    usage       = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    faction_id  = Column(String, ForeignKey("factions.id"), nullable=True, index=True)
    faction_rel = relationship("Factions", back_populates="currency")


# --------- Faction's unit tables --------------------------------------------- 
class UnitCourtOfSevenHeaded(Base):
    __tablename__ = "units_court_of_seven_headed"
 
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    faction     = Column(String, nullable=False)
    allegiance  = Column(String, nullable=False)
    type        = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    faction_id  = Column(String, ForeignKey("factions.id"), nullable=False, index=True)
    faction_rel = relationship("Factions", back_populates="units_court")
    
    __table_args__ = (UniqueConstraint("name", "faction", name="uq_court_name_faction"),)
 
 
class UnitCultOfBlackGrail(Base):
    __tablename__ = "units_cult_of_black_grail"
 
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    faction     = Column(String, nullable=False)
    allegiance  = Column(String, nullable=False)
    type        = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    faction_id  = Column(String, ForeignKey("factions.id"), nullable=False, index=True)
    faction_rel = relationship("Factions", back_populates="units_cult")
    
    __table_args__ = (UniqueConstraint("name", "faction", name="uq_cult_name_faction"),)
 
 
class UnitHereticLegion(Base):
    __tablename__ = "units_heretic_legion"
 
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    faction     = Column(String, nullable=False)
    allegiance  = Column(String, nullable=False)
    type        = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    faction_id  = Column(String, ForeignKey("factions.id"), nullable=False, index=True)
    faction_rel = relationship("Factions", back_populates="units_heretic")
    
    __table_args__ = (UniqueConstraint("name", "faction", name="uq_heretic_name_faction"),)
 
 
class UnitNewAntioch(Base):
    __tablename__ = "units_new_antioch"
 
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    faction     = Column(String, nullable=False)
    allegiance  = Column(String, nullable=False)
    type        = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    faction_id  = Column(String, ForeignKey("factions.id"), nullable=False, index=True)
    faction_rel = relationship("Factions", back_populates="units_new_antioch")
    
    __table_args__ = (UniqueConstraint("name", "faction", name="uq_new_antioch_name_faction"),)
 
 
class UnitTrenchPilgrims(Base):
    __tablename__ = "units_trench_pilgrims"
 
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    faction     = Column(String, nullable=False)
    allegiance  = Column(String, nullable=False)
    type        = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    faction_id  = Column(String, ForeignKey("factions.id"), nullable=False, index=True)
    faction_rel = relationship("Faction", back_populates="units_pilgrims")
    
    __table_args__ = (UniqueConstraint("name", "faction", name="uq_trench_name_faction"),)
 
 
class UnitIronSultanate(Base):
    __tablename__ = "units_iron_sultanate"
 
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    faction     = Column(String, nullable=False)
    allegiance  = Column(String, nullable=False)
    type        = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    faction_id  = Column(String, ForeignKey("factions.id"), nullable=False, index=True)
    faction_rel = relationship("Factions", back_populates="units_sultanate")
    
    __table_args__ = (UniqueConstraint("name", "faction", name="uq_sultanate_name_faction"),)
    
    
