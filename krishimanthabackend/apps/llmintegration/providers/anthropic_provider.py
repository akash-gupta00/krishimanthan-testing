from django.conf import settings
from .base import LLMProvider


class AnthropicProvider(LLMProvider):
    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        import anthropic  # imported lazily so the package is only required if this provider is actually used
        client = anthropic.Anthropic(api_key=settings.LLM_API_KEY)
        response = client.messages.create(
            model=settings.LLM_MODEL,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in response.content if block.type == "text")
