from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..models import User
from ..utils import verify
from ..database import get_db
from ..schemas import UserLogin, TokenSchema
from ..oauth2 import create_access_token

auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/login", response_model=TokenSchema)
def login(
    credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    print(credentials)
    user = db.query(User).filter(User.email == credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="No user with this email"
        )

    if not verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    token = create_access_token(data={"user_id": user.id})

    return {"token": token, "token_type": "bearer"}
