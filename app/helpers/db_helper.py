import json
from typing import List
from app.models.post_model import Post
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.database import AsyncSessionLocal


async def save_post(db: AsyncSession, topic: str, content: str, summary: str, source_urls: List[str], posted: int = 0):
    post = Post(topic=topic, content=content, summary=summary, source_urls=json.dumps(source_urls), posted=posted)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def mark_post_as_posted(db: AsyncSession, post_id: int):
    async with db.begin():
        post = await db.get(Post, post_id)
        if post:
            post.posted = 1
            await db.commit()
            await db.refresh(post)
            return post
    return None


async def get_post_by_id(db: AsyncSession, post_id: int):
    return await db.get(Post, post_id)