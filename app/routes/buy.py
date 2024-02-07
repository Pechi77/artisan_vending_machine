# In routes/user.py or routes/product.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from artisan_vending_machine.app.database import get_db
from artisan_vending_machine.app.core.auth import get_current_user
from artisan_vending_machine.app.schemas import buy
from artisan_vending_machine.app.schemas import user
from artisan_vending_machine.app.services.product_service import buy_product

router = APIRouter()

@router.post("/buy")
def buy(request: buy.BuyRequest, db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    result = buy_product(db, current_user.id, request.product_id, request.quantity)
    return result
