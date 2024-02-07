from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import user
from app.schemas import deposit

def deposit_to_account(db: Session, user_id: int, deposit: deposit.Deposit) -> user.User:
    user = db.query(user.User).filter(user.User.id == user_id).first()
    if user and user.role == "buyer":
        user.balance += deposit.amount
        db.commit()
        db.refresh(user)
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found/ not allowed to deposit")
