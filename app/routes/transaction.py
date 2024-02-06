from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import  services, models
from app.schemas.transaction import PurchaseResponse, PurchaseItem
from app.schemas.deposit import Deposit
from app.database import get_db
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/deposit/", status_code=201)
def deposit(deposit: Deposit, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    updated_user = services.update_user_balance(db, current_user.id, deposit.amount)
    return updated_user

@router.post("/buy/", response_model=PurchaseResponse)
def buy(purchase: PurchaseItem, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return services.process_purchase(db, current_user.id, purchase)

@router.post("/reset/")
def reset_deposit(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    services.reset_user_balance(db, current_user.id)
    return {"msg": "Deposit reset successfully"}
