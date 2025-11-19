"""
LLM Provider implementations
"""
import logging
from typing import Dict
from django.conf import settings
from .base import BaseLLMProvider

logger = logging.getLogger(__name__)


class MockLLMProvider(BaseLLMProvider):
    """Mock LLM provider for development and testing"""

    def generate_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate mock text response"""
        logger.info(f"Mock LLM called with prompt length: {len(prompt)}")
        return "This is a mock response from the LLM. In production, this would be replaced with actual AI-generated content."

    def generate_structured_output(self, prompt: str, schema: Dict) -> Dict:
        """Generate mock structured response"""
        logger.info(f"Mock LLM called for structured output")

        # Return mock data based on schema keys
        mock_data = {}
        for key in schema.get('properties', {}).keys():
            if 'sentiment' in key:
                mock_data[key] = 'neutral'
            elif 'score' in key:
                mock_data[key] = 0.5
            elif 'list' in key or 'array' in schema.get('properties', {}).get(key, {}).get('type', ''):
                mock_data[key] = ['Mock item 1', 'Mock item 2']
            else:
                mock_data[key] = f'Mock {key}'

        return mock_data


class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider"""

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if self.api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                logger.warning("OpenAI library not installed")
                self.client = None
        else:
            self.client = None

    def generate_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate text using OpenAI"""
        if not self.client:
            logger.warning("OpenAI client not initialized, using mock response")
            return MockLLMProvider().generate_text(prompt, max_tokens)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    def generate_structured_output(self, prompt: str, schema: Dict) -> Dict:
        """Generate structured output using OpenAI with JSON mode"""
        if not self.client:
            logger.warning("OpenAI client not initialized, using mock response")
            return MockLLMProvider().generate_structured_output(prompt, schema)

        try:
            import json
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
                    {"role": "user", "content": f"{prompt}\n\nPlease respond with valid JSON matching this schema: {json.dumps(schema)}"}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise


def get_llm_provider() -> BaseLLMProvider:
    """Factory function to get the configured LLM provider"""
    provider_name = settings.LLM_PROVIDER

    if provider_name == 'openai' and settings.OPENAI_API_KEY:
        return OpenAIProvider()
    else:
        logger.info("Using Mock LLM Provider")
        return MockLLMProvider()
