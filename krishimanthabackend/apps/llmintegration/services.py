from django.conf import settings
from .providers.base import LLMProvider, NullProvider


def get_provider() -> LLMProvider:
    """Factory — swap providers purely via the LLM_PROVIDER env var.
    Everything that needs LLM output (views, future management commands,
    future FastAPI service) should call this instead of importing a
    provider class directly, so provider changes never ripple outward."""
    provider = settings.LLM_PROVIDER
    if provider == "anthropic":
        from .providers.anthropic_provider import AnthropicProvider
        return AnthropicProvider()
    if provider == "openai":
        from .providers.openai_provider import OpenAIProvider
        return OpenAIProvider()
    return NullProvider()


class LLMService:
    """Higher-level operations built on top of whichever provider is active.
    Add new agriculture-specific AI features here (e.g. news summarization,
    scheme-eligibility Q&A, chatbot) without touching views or providers."""

    def __init__(self):
        self.provider = get_provider()

    def summarize(self, text: str) -> str:
        prompt = f"Summarize the following agriculture-related text in 2-3 concise sentences, in the same language it is written in:\n\n{text}"
        return self.provider.generate(prompt, max_tokens=300)

    def answer_query(self, question: str, context: str = "") -> str:
        prompt = f"Context:\n{context}\n\nAnswer this farmer's question clearly and simply:\n{question}" if context else question
        return self.provider.generate(prompt, max_tokens=500)
