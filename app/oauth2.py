from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from .models import User
from .database import get_db
from .config import get_settings
from .schemas import TokenDataSchema

s = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=s.access_token_expire_minutes)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, s.secret_key, algorithm=s.algorithm)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, s.secret_key, algorithms=[s.algorithm])
        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception
        token_data = TokenDataSchema(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(User.id == token.id).first()

    return user
