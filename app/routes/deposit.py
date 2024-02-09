from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import deposit_service
from app.core.auth import get_current_user
from app.schemas import deposit
from app.schemas import user

router = APIRouter()

@router.post("/deposit/")
def deposit(deposit: deposit.Deposit, db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    try:
        return deposit_service.deposit_to_account(db, current_user.id, deposit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

