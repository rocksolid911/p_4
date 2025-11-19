"""
Recommendation service using PostgresML
"""
import logging
from typing import List, Dict
from django.conf import settings
from django.db import connection

from content.models import Bill, NewsArticle, UserInteraction

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service for generating content recommendations using PostgresML"""

    def __init__(self):
        self.pgml_enabled = settings.PGML_ENABLED

    def get_recommendations_for_user(self, user_id: int, limit: int = 20) -> List[Dict]:
        """
        Get personalized content recommendations for a user

        Args:
            user_id: User ID
            limit: Maximum number of recommendations

        Returns:
            List of recommendation dicts with type, id, title, score
        """
        if not self.pgml_enabled:
            logger.info("PostgresML disabled, using fallback recommendations")
            return self._get_fallback_recommendations(user_id, limit)

        try:
            return self._get_pgml_recommendations(user_id, limit)
        except Exception as e:
            logger.error(f"PostgresML recommendation failed: {e}")
            return self._get_fallback_recommendations(user_id, limit)

    def _get_pgml_recommendations(self, user_id: int, limit: int) -> List[Dict]:
        """
        Generate recommendations using PostgresML

        This is a placeholder implementation. In production, you would:
        1. Train a model using user interactions
        2. Use collaborative filtering or content-based filtering
        3. Query the trained model for recommendations
        """

        # For now, use a simple query-based approach
        # In production, replace this with actual PostgresML model predictions

        with connection.cursor() as cursor:
            # Get user's interaction history
            cursor.execute("""
                SELECT object_type, object_id, interaction_type, created_at
                FROM user_interactions
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT 100
            """, [user_id])

            interactions = cursor.fetchall()

        # Get user's preferred topics from their interaction history
        user_topics = self._extract_user_topics(user_id)

        # Get recommendations based on topics and recency
        recommendations = []

        # Recommend bills
        bills = Bill.objects.filter(topics__overlap=user_topics)[:limit // 2]
        for bill in bills:
            recommendations.append({
                'type': 'bill',
                'id': bill.id,
                'title': bill.title,
                'score': 0.8,  # Placeholder score
                'reason': 'Based on your interests',
            })

        # Recommend news
        news = NewsArticle.objects.filter(topics__overlap=user_topics)[:limit // 2]
        for article in news:
            recommendations.append({
                'type': 'news',
                'id': article.id,
                'title': article.title,
                'score': 0.7,  # Placeholder score
                'reason': 'Based on your reading history',
            })

        return recommendations[:limit]

    def _get_fallback_recommendations(self, user_id: int, limit: int) -> List[Dict]:
        """
        Fallback recommendations when PostgresML is not available

        Uses simple heuristics:
        1. User's recent interactions to infer interests
        2. Popular/recent content
        3. Diversity across content types
        """
        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            user = User.objects.get(id=user_id)
            user_interests = user.interests or []
            user_state = user.state
        except User.DoesNotExist:
            user_interests = []
            user_state = None

        recommendations = []

        # Get recent bills matching user interests or state
        bills_query = Bill.objects.all()
        if user_interests:
            bills_query = bills_query.filter(topics__overlap=user_interests)
        if user_state:
            bills_query = bills_query.filter(state=user_state)

        bills = bills_query.order_by('-introduced_on', '-created_at')[:limit // 2]
        for bill in bills:
            recommendations.append({
                'type': 'bill',
                'id': bill.id,
                'title': bill.title,
                'score': 0.75,
                'reason': self._get_recommendation_reason(bill, user_interests, user_state),
            })

        # Get recent news matching user interests
        news_query = NewsArticle.objects.all()
        if user_interests:
            news_query = news_query.filter(topics__overlap=user_interests)

        news = news_query.order_by('-published_at', '-created_at')[:limit // 2]
        for article in news:
            recommendations.append({
                'type': 'news',
                'id': article.id,
                'title': article.title,
                'score': 0.7,
                'reason': self._get_recommendation_reason(article, user_interests),
            })

        # Shuffle to mix bills and news
        import random
        random.shuffle(recommendations)

        return recommendations[:limit]

    def _extract_user_topics(self, user_id: int) -> List[str]:
        """Extract topics from user's interaction history"""
        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            user = User.objects.get(id=user_id)
            return user.interests or []
        except User.DoesNotExist:
            return []

    def _get_recommendation_reason(self, obj, user_interests, user_state=None) -> str:
        """Generate a reason for the recommendation"""
        reasons = []

        if hasattr(obj, 'topics') and obj.topics:
            matching_topics = set(obj.topics) & set(user_interests)
            if matching_topics:
                topic = list(matching_topics)[0]
                reasons.append(f"Matches your interest in {topic}")

        if hasattr(obj, 'state') and obj.state and obj.state == user_state:
            reasons.append(f"From your state")

        if not reasons:
            reasons.append("Trending now")

        return reasons[0]

    def train_model(self):
        """
        Train PostgresML recommendation model

        This is a placeholder for production implementation.
        In production, you would:
        1. Create a training dataset from user interactions
        2. Use PostgresML to train a collaborative filtering or content-based model
        3. Store the trained model for inference
        """
        if not self.pgml_enabled:
            logger.warning("PostgresML not enabled, skipping model training")
            return

        logger.info("Model training not yet implemented - using rule-based recommendations")
        # TODO: Implement actual PostgresML model training
        # Example:
        # pgml.train(
        #     project_name='loksathi_recommendations',
        #     task='regression',
        #     relation_name='user_interactions',
        #     y_column_name='score',
        #     algorithm='xgboost'
        # )
