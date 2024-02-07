from fastapi import HTTPException
from sqlalchemy.orm import Session
from artisan_vending_machine.app.models.user import User
from artisan_vending_machine.app.schemas.user import UserCreate, UserUpdate
from artisan_vending_machine.app.core.security import get_password_hash, verify_password

def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password, email=user.email, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> User:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def update_user(db: Session, username: str, user_update: UserUpdate) -> User:
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        return None  # User not found
    
    if user_update.password:
        hashed_password = get_password_hash(user_update.password)
        db_user.hashed_password = hashed_password
    if user_update.email:
        db_user.email = user_update.email

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, username: str) -> bool:
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        return False 
    
    db.delete(db_user)
    db.commit()
    return True


def reset_deposit(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
        
    if user and user.role == "buyer":
        user.balance = 0
        db.commit()
        return {"detail": "Deposit reset successfully"}
    
    raise HTTPException(status_code=403, detail="Only buyers can reset their deposit")