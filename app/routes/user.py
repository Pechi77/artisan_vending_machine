from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import user_service
from app.schemas.user import UserCreate, User  # Make sure to import UserCreate
from app.database import get_db  # Import get_db here

router = APIRouter()


@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):  # Use UserCreate
    db_user = user_service.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_service.create_user(db=db, user=user)
