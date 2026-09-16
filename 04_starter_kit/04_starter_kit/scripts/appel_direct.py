from google import genai

from backend.config import settings


client = genai.Client(api_key=settings.gemini_api_key)

response = client.models.generate_content(
    model=settings.default_model,
    contents="Explique le RGPD en 3 phrases.",
)

print(response.text)
