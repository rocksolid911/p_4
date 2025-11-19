"""
News Bias and Sentiment Analysis Service
"""
import logging
from typing import Dict
from .base import BaseAIService
from .llm_provider import get_llm_provider

logger = logging.getLogger(__name__)


class NewsBiasAnalyzerService(BaseAIService):
    """Service for analyzing news article bias and sentiment"""

    def __init__(self):
        self.llm = get_llm_provider()

    def process(self, article_content: str, language_code: str = 'en') -> Dict:
        """
        Analyze a news article for bias and sentiment

        Args:
            article_content: Full text of the news article
            language_code: Language code for analysis

        Returns:
            Dictionary with analysis results
        """
        try:
            return self._analyze_article(article_content, language_code)
        except Exception as e:
            logger.error(f"Failed to analyze article: {e}")
            return self._get_fallback_analysis()

    def _analyze_article(self, content: str, language_code: str) -> Dict:
        """Perform bias and sentiment analysis"""

        # Truncate content if too long
        max_content_length = 4000
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."

        prompt = f"""Analyze this news article for bias, sentiment, and propaganda.

Article Content:
{content}

Please provide:
1. Overall sentiment (positive, neutral, or negative)
2. Political leaning (neutral, govt_leaning, opposition_leaning, or unclear)
3. Propaganda score (0.0 to 1.0, where 0 is no propaganda and 1 is high propaganda)
4. Whether emotional language is detected (true/false)
5. List of emotional or loaded phrases found in the article
6. A clear explanation of why the article is classified this way

Important context: This is for Indian political content. Consider Indian political context.

Respond as valid JSON with these keys:
- sentiment (string: "positive", "neutral", or "negative")
- leaning (string: "neutral", "govt_leaning", "opposition_leaning", or "unclear")
- propaganda_score (number: 0.0 to 1.0)
- emotional_language_detected (boolean)
- emotional_phrases (array of strings)
- explanation (string)
"""

        schema = {
            "type": "object",
            "properties": {
                "sentiment": {"type": "string"},
                "leaning": {"type": "string"},
                "propaganda_score": {"type": "number"},
                "emotional_language_detected": {"type": "boolean"},
                "emotional_phrases": {"type": "array"},
                "explanation": {"type": "string"}
            }
        }

        result = self.llm.generate_structured_output(prompt, schema)

        # Validate and normalize the response
        return {
            'sentiment': self._validate_sentiment(result.get('sentiment', 'neutral')),
            'leaning': self._validate_leaning(result.get('leaning', 'unclear')),
            'propaganda_score': max(0.0, min(1.0, float(result.get('propaganda_score', 0.0)))),
            'emotional_language_detected': bool(result.get('emotional_language_detected', False)),
            'emotional_phrases': result.get('emotional_phrases', []),
            'explanation': result.get('explanation', ''),
        }

    def _validate_sentiment(self, sentiment: str) -> str:
        """Validate sentiment value"""
        valid_sentiments = ['positive', 'neutral', 'negative']
        return sentiment if sentiment in valid_sentiments else 'neutral'

    def _validate_leaning(self, leaning: str) -> str:
        """Validate political leaning value"""
        valid_leanings = ['neutral', 'govt_leaning', 'opposition_leaning', 'unclear']
        return leaning if leaning in valid_leanings else 'unclear'

    def _get_fallback_analysis(self) -> Dict:
        """Return a fallback analysis when AI processing fails"""
        return {
            'sentiment': 'neutral',
            'leaning': 'unclear',
            'propaganda_score': 0.0,
            'emotional_language_detected': False,
            'emotional_phrases': [],
            'explanation': 'Analysis could not be completed. Please try again.',
        }
