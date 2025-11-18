"""
Serializers for content models
"""
from rest_framework import serializers
from .models import Bill, BillSummary, NewsArticle, NewsAnalysis, UserInteraction


class BillSummarySerializer(serializers.ModelSerializer):
    """Serializer for BillSummary"""

    class Meta:
        model = BillSummary
        fields = [
            'id', 'bill', 'language_code', 'summary_short',
            'summary_detailed', 'pros', 'cons', 'key_points',
            'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BillSerializer(serializers.ModelSerializer):
    """Serializer for Bill with optional summaries"""
    summaries = BillSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Bill
        fields = [
            'id', 'title', 'full_text', 'source_url',
            'parliament_house', 'introduced_on', 'status',
            'state', 'topics', 'summaries',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BillListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for bill lists"""
    has_summary = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = [
            'id', 'title', 'parliament_house', 'introduced_on',
            'status', 'state', 'topics', 'has_summary', 'created_at'
        ]

    def get_has_summary(self, obj):
        return obj.summaries.exists()


class NewsAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for NewsAnalysis"""

    class Meta:
        model = NewsAnalysis
        fields = [
            'id', 'article', 'sentiment', 'leaning',
            'propaganda_score', 'explanation',
            'emotional_language_detected', 'emotional_phrases',
            'language_code', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NewsArticleSerializer(serializers.ModelSerializer):
    """Serializer for NewsArticle with optional analyses"""
    analyses = NewsAnalysisSerializer(many=True, read_only=True)

    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'content', 'source_url',
            'source_name', 'published_at', 'topics',
            'language_code', 'analyses',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NewsArticleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for news lists"""
    has_analysis = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'source_name', 'published_at',
            'topics', 'language_code', 'has_analysis', 'created_at'
        ]

    def get_has_analysis(self, obj):
        return obj.analyses.exists()


class UserInteractionSerializer(serializers.ModelSerializer):
    """Serializer for UserInteraction"""

    class Meta:
        model = UserInteraction
        fields = ['id', 'user', 'object_type', 'object_id', 'interaction_type', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CreateInteractionSerializer(serializers.ModelSerializer):
    """Serializer for creating interactions"""

    class Meta:
        model = UserInteraction
        fields = ['object_type', 'object_id', 'interaction_type']
