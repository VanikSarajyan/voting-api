from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import post, user, auth, vote

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"welcome": "voting-api"}


app.include_router(post.posts_router)
app.include_router(user.users_router)
app.include_router(auth.auth_router)
app.include_router(vote.vote_router)
