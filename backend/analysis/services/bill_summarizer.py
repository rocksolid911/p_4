"""
Bill Summarization Service
"""
import logging
from typing import List, Dict
from django.conf import settings
from .base import BaseAIService
from .llm_provider import get_llm_provider

logger = logging.getLogger(__name__)


class BillSummarizerService(BaseAIService):
    """Service for summarizing legislative bills"""

    def __init__(self):
        self.llm = get_llm_provider()

    def process(self, bill_text: str, language_codes: List[str] = None) -> Dict[str, Dict]:
        """
        Summarize a bill in multiple languages

        Args:
            bill_text: Full text of the bill
            language_codes: List of language codes (e.g., ['en', 'hi'])

        Returns:
            Dictionary mapping language codes to summary data
        """
        if language_codes is None:
            language_codes = ['en']

        summaries = {}

        for lang_code in language_codes:
            try:
                summary = self._summarize_in_language(bill_text, lang_code)
                summaries[lang_code] = summary
            except Exception as e:
                logger.error(f"Failed to summarize bill in {lang_code}: {e}")
                summaries[lang_code] = self._get_fallback_summary(lang_code)

        return summaries

    def _summarize_in_language(self, bill_text: str, language_code: str) -> Dict:
        """Generate summary in a specific language"""

        language_names = {
            'en': 'English',
            'hi': 'Hindi',
            'mr': 'Marathi',
            'te': 'Telugu',
            'ta': 'Tamil',
            'bn': 'Bengali',
            'gu': 'Gujarati',
            'kn': 'Kannada',
        }

        language_name = language_names.get(language_code, 'English')

        # Truncate bill text if too long
        max_bill_length = 4000
        if len(bill_text) > max_bill_length:
            bill_text = bill_text[:max_bill_length] + "..."

        prompt = f"""Analyze this legislative bill and provide a comprehensive summary in {language_name}.

Bill Text:
{bill_text}

Please provide:
1. A short summary (2-3 sentences)
2. A detailed summary (1-2 paragraphs)
3. Key points (3-5 bullet points)
4. Pros (potential benefits, 2-4 points)
5. Cons (potential concerns or drawbacks, 2-4 points)

Respond in {language_name} and format the response as valid JSON with these keys:
- summary_short
- summary_detailed
- key_points (array)
- pros (array)
- cons (array)
"""

        schema = {
            "type": "object",
            "properties": {
                "summary_short": {"type": "string"},
                "summary_detailed": {"type": "string"},
                "key_points": {"type": "array"},
                "pros": {"type": "array"},
                "cons": {"type": "array"}
            }
        }

        result = self.llm.generate_structured_output(prompt, schema)

        # Ensure all fields are present
        return {
            'summary_short': result.get('summary_short', ''),
            'summary_detailed': result.get('summary_detailed', ''),
            'key_points': result.get('key_points', []),
            'pros': result.get('pros', []),
            'cons': result.get('cons', []),
        }

    def _get_fallback_summary(self, language_code: str) -> Dict:
        """Return a fallback summary when AI processing fails"""
        messages = {
            'en': 'Summary generation failed. Please try again.',
            'hi': 'सारांश उत्पन्न करने में विफल। कृपया पुन: प्रयास करें।',
        }

        message = messages.get(language_code, messages['en'])

        return {
            'summary_short': message,
            'summary_detailed': message,
            'key_points': [],
            'pros': [],
            'cons': [],
        }
