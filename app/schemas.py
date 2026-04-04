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
        
# ------- NONE --------------------------------------------------------