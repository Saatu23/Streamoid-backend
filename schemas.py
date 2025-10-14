from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    sku: str
    name: str
    brand: str
    color: Optional[str]
    size: Optional[str]
    mrp: int
    price: int
    quantity: int
    class Config:
        orm_mode = True
