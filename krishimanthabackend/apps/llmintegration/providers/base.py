from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Common interface every LLM provider must implement. Add a new
    provider by subclassing this and registering it in `get_provider()`
    (services.py) — nothing else in the codebase needs to change."""

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        ...


class NullProvider(LLMProvider):
    """Used when LLM_PROVIDER=none — keeps every endpoint callable without
    an API key configured, returning a clear message instead of crashing."""

    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        return "LLM provider not configured. Set LLM_PROVIDER and LLM_API_KEY in .env to enable this feature."
