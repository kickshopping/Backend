from pydantic import BaseModel
from datetime import datetime
from typing import List

class PurchaseItemOut(BaseModel):
    product_name: str
    quantity: int
    unit_price: float
    total: float

class PurchaseTicket(BaseModel):
    ticket_id: str
    purchase_date: datetime
    items: List[PurchaseItemOut]
    total_amount: float
    user_id: int
    user_name: str