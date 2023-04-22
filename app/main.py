from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from functools import lru_cache
from psycopg2.extras import RealDictCursor
import time

from .config import Settings

app = FastAPI()


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()


# Schema
class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = True


class UpdatePostSchema(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]


while True:
    try:
        conn = psycopg2.connect(
            host=settings.db_hostname,
            database=settings.db_name,
            user=settings.db_username,
            password=settings.db_password,
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Database connection failed")
        print(error)
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "welcome to my api"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


# Path parameter
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id}"
        )
    return {"data": post}


# For default status code put it in decorator
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: PostSchema):
    # For handling SQL injections
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: PostSchema):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, id),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id}"
        )
    return {"data": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id}"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
