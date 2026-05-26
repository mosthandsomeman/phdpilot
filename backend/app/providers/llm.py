"""LLM provider abstraction — do not hardcode a single vendor."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    content: str
    input_tokens: int
    output_tokens: int
    model_name: str


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system: str | None = None, max_tokens: int = 4096) -> LLMResponse:
        pass


class DeepSeekProvider(LLMProvider):
    """Placeholder — wire httpx client in Phase 3."""

    async def generate(self, prompt: str, system: str | None = None, max_tokens: int = 4096) -> LLMResponse:
        raise NotImplementedError("DeepSeek integration planned for Phase 3")
