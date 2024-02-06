from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import schemas, database
from app.models import user
from app.core import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)) -> user.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(user.User).filter(user.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
