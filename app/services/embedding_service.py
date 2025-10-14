from typing import List
from app.configs.config import settings
from google import genai
import asyncio



EMBED_MODEL = "text-embedding-004"


def _get_genai_client():
    if genai is None:
        raise RuntimeError("google-genai is not installed. pip install google-genai")
    return genai.Client(api_key=settings.GOOGLE_API_KEY)


async def embed_texts(texts: List[str]) -> List[List[float]]:

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _embed_sync, texts)


def _embed_sync(texts: List[str]) -> List[List[float]]:
    client = _get_genai_client()

    try:
        embeddings = []
        resp = client.models.embed_content(model=EMBED_MODEL, contents=texts)

        embedding = resp.embeddings[0].values
        embeddings.append(embedding)
        return embeddings
    except Exception as e:
        raise RuntimeError(f"Embedding generation failed: {e}")