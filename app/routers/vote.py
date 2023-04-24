from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

from ..models import User, Vote, Post
from ..database import get_db
from ..schemas import VoteSchema
from ..oauth2 import get_current_user

vote_router = APIRouter(prefix="/vote", tags=["Vote"])


@vote_router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: VoteSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist.",
        )

    vote_query = db.query(Vote).filter(
        Vote.post_id == vote.post_id, Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )
        vote_query.delete()
        db.commit()
        return {"message": "successfully unvoted"}
