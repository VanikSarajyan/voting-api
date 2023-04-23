from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session

from . import models
from .utils import hash
from .database import engine, get_db
from .schemas import (
    PostCreateSchema,
    PostUpdateSchema,
    PostResponseSchema,
    UserCreateSchema,
    UserResponseSchema,
)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "welcome to my api"}


@app.get("/posts", response_model=list[PostResponseSchema])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Path parameter
@app.get("/posts/{id}", response_model=PostResponseSchema)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id}"
        )
    return post


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema
)
def create_post(post: PostCreateSchema, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.put(
    "/posts/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=PostResponseSchema,
)
def update_post(id: int, post: PostUpdateSchema, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_query.first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id}"
        )

    post_dict = post.dict(exclude_unset=True)
    for key, value in post_dict.items():
        setattr(db_post, key, value)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id}"
        )
    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/users", response_model=list[UserResponseSchema])
def get_users(db: Session = Depends(get_db)):
    posts = db.query(models.User).all()
    return posts


@app.get("/users/{id}", response_model=UserResponseSchema)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with id: {id}"
        )
    return user


@app.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema
)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    user.password = hash(user.password)

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
