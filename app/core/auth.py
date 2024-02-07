from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from artisan_vending_machine.app import schemas, database
from artisan_vending_machine.app.models import user
from artisan_vending_machine.app.core import settings

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

    uservalue = db.query(user.User).filter(user.User.username == username).first()
    if uservalue is None:
        raise credentials_exception
    return uservalue
