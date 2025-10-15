from pydantic import BaseModel
from typing import Optional, List


class PostCreate(BaseModel):
    topic: str
    post_length: Optional[str] = "short"
    auto_post: Optional[bool] = False


class PostOut(BaseModel):
    id: int
    topic: str
    content: str
    summary: Optional[str]
    source_urls: Optional[List[str]] = []
    posted: int


class Config:
    orm_mode = True