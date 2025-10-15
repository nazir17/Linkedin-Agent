from typing import List, Dict
from app.configs.config import settings
from google import genai





MODEL = "gemini-2.0-flash-exp"


def _get_genai_client():
    if genai is None:
        raise RuntimeError("google-genai is not installed. pip install google-genai")
    client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    return client


def generate_linkedin_post(topic: str, context_snippets: List[str], length: str = "short") -> Dict:
    client = _get_genai_client()
    prompt = (
        f"You are a social media copywriter. Create a LinkedIn post about '{topic}'.\n\n"
        "Context (recent news snippets):\n"
    )
    for i, s in enumerate(context_snippets):
        prompt += f"{i+1}. {s}\n"
    prompt += (
        "\nRequirements:\n"
        "- Hook in first line (attention grabbing)\n"
        "- 2-4 lines max for short, 4-8 lines for long\n"
        "- Add 3 relevant hashtags at the end\n"
        "- Add 1 short CTA (e.g., 'Thoughts?')\n"
    )
    if length == "short":
        prompt += "\nTone: professional, concise\n"
    else:
        prompt += "\nTone: professional, slightly detailed\n"


    resp = client.models.generate_content(model=MODEL, contents=prompt)
    
    text = None
    try:
        if hasattr(resp, 'content'):
            text = resp.content
        elif hasattr(resp, 'candidates') and resp.candidates:
            text = resp.candidates[0].content
        elif hasattr(resp, 'text'):
            text = resp.text
        else:
            text = str(resp)
    except Exception:
        text = str(resp)


    return {"content": text, "summary": (context_snippets[0] if context_snippets else "")}
