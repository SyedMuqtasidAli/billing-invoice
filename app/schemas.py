# schemas.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class InvoiceItemCreate(BaseModel):
    description: str
    quantity: int
    unit_price: float

class InvoiceCreate(BaseModel):
    customer_name: str
    address: Optional[str] = None
    tax_rate: float = 15.0
    adv_tax: float = 0.0
    discount: float = 0.0
    items: List[InvoiceItemCreate]

class InvoiceItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # pydantic v2
    id: int
    description: str
    quantity: int
    unit_price: float
    total_price: float

class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # pydantic v2
    id: int
    customer_name: str
    address: Optional[str]
    date: datetime
    total_amount: float
    tax_rate: float
    adv_tax: float
    discount: float
    net_amount: float
    items: List[InvoiceItemResponse]
