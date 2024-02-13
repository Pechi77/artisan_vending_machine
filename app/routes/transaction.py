from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import  services, models
from app.services import product_service
from app.services import user_service
from app.services import deposit_service
from app.schemas.transaction import PurchaseResponse, PurchaseItem
from app.schemas.deposit import Deposit
from app.database import get_db
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/deposit/", status_code=201)
def deposit(deposit: Deposit, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    updated_user = deposit_service.deposit_to_account(db, current_user.id, deposit)
    return updated_user

@router.post("/buy/", response_model=PurchaseResponse)
def buy(purchase: PurchaseItem, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return product_service.buy_product(db, current_user.id, purchase.product_id, purchase.quantity)

@router.post("/reset/")
def reset_deposit(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return user_service.reset_deposit(db, current_user.id)
