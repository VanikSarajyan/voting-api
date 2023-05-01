from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

from ..utils import hash
from ..models import User
from ..database import get_db
from ..schemas import UserCreateSchema, UserResponseSchema

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/", response_model=list[UserResponseSchema])
def get_users(db: Session = Depends(get_db)):
    posts = db.query(User).all()
    return posts


@users_router.get("/{id}", response_model=UserResponseSchema)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with id: {id}"
        )
    return user


@users_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema
)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    user.password = hash(user.password)
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user.email} already exists.",
        )

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
