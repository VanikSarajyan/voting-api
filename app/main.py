from fastapi import FastAPI, Response, status, HTTPException, Depends

from . import models
from .database import engine
from .routers import post, user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(post.posts_router)
app.include_router(user.users_router)
