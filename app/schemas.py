from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


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


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    id: Optional[str] = None
