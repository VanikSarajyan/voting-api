from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


# Schema
class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class UpdatePostSchema(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]
    rating: Optional[int] = None


id = 3
my_posts = [
    {"id": 1, "title": "ex title", "content": "ex content"},
    {"id": 2, "title": "ex title2", "content": "ex content2"},
]


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


def update(post, new_post):
    for k in post.keys():
        if new_post[k] is not None:
            post[k] = new_post[k]


@app.get("/")
def root():
    return {"message": "welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# Path parameter
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    filtered = list(filter((lambda x: x["id"] == id), my_posts))

    if len(filtered) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id}"
        )
    else:
        return {"data": filtered[0]}


# For default status code put it in decorator
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: PostSchema):
    global id
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts.append(post_dict)
    id += 1
    return {"data": post_dict}


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: UpdatePostSchema):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id}"
        )
    post_dict = post.dict()
    post_dict["id"] = id
    old_post = my_posts[index]
    update(old_post, post_dict)
    return {"data": old_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id}"
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
