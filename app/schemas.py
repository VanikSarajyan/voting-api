from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class PostBaseSchema(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreateSchema(PostBaseSchema):
    pass


class PostUpdateSchema(PostBaseSchema):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]


class PostResponseSchema(PostBaseSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
