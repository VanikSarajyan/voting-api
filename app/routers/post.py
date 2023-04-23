from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter

from ..models import Post, User
from ..database import get_db
from ..oauth2 import get_current_user
from ..schemas import PostCreateSchema, PostUpdateSchema, PostResponseSchema

posts_router = APIRouter(prefix="/posts", tags=["Posts"])


@posts_router.get("/", response_model=list[PostResponseSchema])
def get_posts(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    posts = db.query(Post).all()
    return posts


@posts_router.get("/{id}", response_model=PostResponseSchema)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id}"
        )
    return post


@posts_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema
)
def create_post(
    post: PostCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(current_user)
    new_post = Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@posts_router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=PostResponseSchema,
)
def update_post(
    id: int,
    post: PostUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post_query = db.query(Post).filter(Post.id == id)
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


@posts_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post_query = db.query(Post).filter(Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id}"
        )
    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
