from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, services
from app.dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/deposit/")
def deposit(deposit: schemas.Deposit, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    try:
        return services.deposit_to_account(db, current_user.id, deposit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
