from pydantic import BaseModel
from typing import List

class PurchaseItem(BaseModel):
    product_id: int
    quantity: int

class PurchaseResponse(BaseModel):
    total_spent: float
    products_purchased: List[PurchaseItem]
    change: float


