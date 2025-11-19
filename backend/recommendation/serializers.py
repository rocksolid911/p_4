"""
Serializers for recommendations
"""
from rest_framework import serializers
from content.serializers import BillListSerializer, NewsArticleListSerializer
from content.models import Bill, NewsArticle


class RecommendationSerializer(serializers.Serializer):
    """Serializer for a single recommendation"""
    type = serializers.ChoiceField(choices=['bill', 'news'])
    id = serializers.IntegerField()
    title = serializers.CharField()
    score = serializers.FloatField()
    reason = serializers.CharField()
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        """Get the full content object"""
        if obj['type'] == 'bill':
            try:
                bill = Bill.objects.get(id=obj['id'])
                return BillListSerializer(bill).data
            except Bill.DoesNotExist:
                return None
        elif obj['type'] == 'news':
            try:
                article = NewsArticle.objects.get(id=obj['id'])
                return NewsArticleListSerializer(article).data
            except NewsArticle.DoesNotExist:
                return None
        return None
