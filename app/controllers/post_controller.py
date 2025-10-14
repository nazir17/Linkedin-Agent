from fastapi import APIRouter, HTTPException
from app.schemas.post_schema import PostCreate, PostOut
from app.services.post_service import create_post_flow, publish_existing_post


router = APIRouter()


@router.post("/generate", response_model=PostOut)
async def generate_post(payload: PostCreate):
    try:
        post = await create_post_flow(payload.topic, payload.post_length, payload.auto_post)
        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/publish/{post_id}")
async def publish_post(post_id: int):
    try:
        ok = await publish_existing_post(post_id)
        if ok:
            return {"success": True}
        else:
            raise HTTPException(status_code=500, detail="Failed to publish")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))