from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.services import user_service
from app.schemas.user import UserCreate, User, UserUpdate
from app.database import get_db  
from app.core import auth
from app.services.auth_service import create_access_token
from app.core.auth import get_current_user
router = APIRouter()

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/{username}", response_model=User)
def read_user(username: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.username != username and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user_service.get_user_by_username(db, username)


@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):  # Use UserCreate
    db_user = user_service.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_service.create_user(db=db, user=user)


@router.put("/users/{username}", response_model=User)
def update_user(username: str, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.username != username and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user_service.update_user(db, username, user_update)


@router.delete("/users/{username}", response_model=User)
def delete_user(username: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.username != username and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user_service.delete_user(db, username)


@router.post("/reset")
def reset_user_deposit(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_service.reset_deposit(db, current_user.id)