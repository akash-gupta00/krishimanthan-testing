from django.conf import settings
from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        from openai import OpenAI  # imported lazily, same reasoning as AnthropicProvider
        client = OpenAI(api_key=settings.LLM_API_KEY)
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
