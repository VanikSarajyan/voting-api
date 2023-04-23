from fastapi import FastAPI, Response, status, HTTPException, Depends

from .models import Base
from .database import engine
from .routers import post, user, auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(post.posts_router)
app.include_router(user.users_router)
app.include_router(auth.auth_router)
