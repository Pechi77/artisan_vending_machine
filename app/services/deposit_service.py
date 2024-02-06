from sqlalchemy.orm import Session
from app.models import User
from app.schemas import Deposit

def deposit_to_account(db: Session, user_id: int, deposit: Deposit) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.balance += deposit.amount
        db.commit()
        db.refresh(user)
        return user
    else:
        raise Exception("User not found")
