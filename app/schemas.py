from typing import Any
from pydantic import BaseModel

# ------- Items --------------------------------------------------------
class ItemBase(BaseModel):
    name: str
    description: str | None = None
    class_name: str

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True

# ------- Currency --------------------------------------------------------
class CurrencyBase(BaseModel):
    coinage: str
    usage: str
    description: str | None = None

class CurrencyCreate(CurrencyBase):
    pass

class CurrencyResponse(CurrencyBase):
    id: int
    class Config:
        from_attributes = True


# ------- Units --------------------------------------------------------
class UnitBase(BaseModel):
    name: str
    faction: str
    allegiance: str
    type: str
    description: str | None = None

class UnitCreate(UnitBase):
    pass

class UnitResponse(UnitBase):
    id: int
    class Config:
        from_attributes = True


# ------- FACTIONS --------------------------------------------------------
class FactionsBase(BaseModel):
    id: str
    name: str
    full_name: str         | None = None
    affiliation: str
    religion: str          | None = None
    capital: str           | None = None
    language: list[str]    | None = None
    currency: str          | None = None
    description: str       | None = None
    government: dict[str, Any]   | None = None
    sub_factions: dict[str, Any] | None = None
    units: dict[str, Any]        | None = None
    lore: dict[str, Any]         | None = None

class FactionCreate(FactionsBase):
    pass

class FactionResponse(FactionsBase):
    class Config:
        from_attribute = True

# ------- NONE --------------------------------------------------------
