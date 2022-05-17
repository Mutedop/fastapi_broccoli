from pydantic import BaseModel

from users.schemas import ShowUser


class BlogBase(BaseModel):
    title: str
    text: str


class Blog(BlogBase):
    class Config:
        orm_mode = True


class ShowBlog(Blog):
    title: str
    text: str
    owner: ShowUser

    class Config:
        orm_mode = True
