from google import genai

from app.core.config import settings

_client = genai.Client(api_key=settings.GEMINI_API_KEY)


DEFAULT_MODEL = "gemini-3.1-flash-lite-preview"


def get_client() -> genai.Client:
    return _client
