"""
Base classes for AI services
"""
from abc import ABC, abstractmethod
from typing import Dict, List


class BaseAIService(ABC):
    """Base class for all AI services"""

    @abstractmethod
    def process(self, *args, **kwargs):
        """Process the AI task"""
        pass


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""

    @abstractmethod
    def generate_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate text from a prompt"""
        pass

    @abstractmethod
    def generate_structured_output(self, prompt: str, schema: Dict) -> Dict:
        """Generate structured output from a prompt"""
        pass
