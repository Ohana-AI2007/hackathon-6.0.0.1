import os
import httpx
from dotenv import load_dotenv

load_dotenv()

AGENTS = {
    name: (os.getenv(f"{name.upper()}_AGENT_URL") or "").rstrip("/")
    for name in ("video", "pdf", "blog", "tutor")
}

KEYWORDS = {
    "video": ["video", "lecture", "youtube", "watch"],
    "pdf":   ["pdf", "document", "file", "upload"],
    "blog":  ["blog", "write", "create", "content", "article"],
    "tutor": ["tutor", "explain", "teach", "doubt"],
}


def route(text: str) -> str:
    """Request padh ke sahi agent chunta hai."""
    t = text.lower()
    return next((n for n, words in KEYWORDS.items() if any(w in t for w in words)), "pdf")


async def status() -> dict:
    """Koi bhi HTTP reply aaye to agent online."""
    out = {}
    async with httpx.AsyncClient(timeout=3) as client:
        for name, url in AGENTS.items():
            try:
                await client.get(url)
                out[name] = True
            except Exception:
                out[name] = False
    return out