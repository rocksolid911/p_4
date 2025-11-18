"""
Views for content models
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Bill, BillSummary, NewsArticle, NewsAnalysis, UserInteraction
from .serializers import (
    BillSerializer,
    BillListSerializer,
    BillSummarySerializer,
    NewsArticleSerializer,
    NewsArticleListSerializer,
    NewsAnalysisSerializer,
    CreateInteractionSerializer,
)
from analytics.mixpanel_client import track_event


class BillViewSet(viewsets.ModelViewSet):
    """ViewSet for Bill model"""
    queryset = Bill.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'parliament_house', 'state']
    search_fields = ['title', 'full_text']
    ordering_fields = ['introduced_on', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return BillListSerializer
        return BillSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        # Track view event if user is authenticated
        if request.user.is_authenticated:
            bill = self.get_object()
            UserInteraction.objects.create(
                user=request.user,
                object_type='bill',
                object_id=bill.id,
                interaction_type='view'
            )
            track_event(request.user.id, 'bill_viewed', {
                'bill_id': bill.id,
                'bill_title': bill.title,
            })

        return response

    @action(detail=True, methods=['get'])
    def summaries(self, request, pk=None):
        """Get summaries for a specific bill"""
        bill = self.get_object()
        language = request.query_params.get('language', None)

        summaries = bill.summaries.all()
        if language:
            summaries = summaries.filter(language_code=language)

        serializer = BillSummarySerializer(summaries, many=True)
        return Response(serializer.data)


class NewsArticleViewSet(viewsets.ModelViewSet):
    """ViewSet for NewsArticle model"""
    queryset = NewsArticle.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['source_name', 'language_code']
    search_fields = ['title', 'content']
    ordering_fields = ['published_at', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsArticleListSerializer
        return NewsArticleSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        # Track view event if user is authenticated
        if request.user.is_authenticated:
            article = self.get_object()
            UserInteraction.objects.create(
                user=request.user,
                object_type='news',
                object_id=article.id,
                interaction_type='view'
            )
            track_event(request.user.id, 'news_article_viewed', {
                'article_id': article.id,
                'article_title': article.title,
            })

        return response

    @action(detail=True, methods=['get'])
    def analyses(self, request, pk=None):
        """Get analyses for a specific article"""
        article = self.get_object()
        language = request.query_params.get('language', None)

        analyses = article.analyses.all()
        if language:
            analyses = analyses.filter(language_code=language)

        serializer = NewsAnalysisSerializer(analyses, many=True)
        return Response(serializer.data)


class UserInteractionViewSet(viewsets.ModelViewSet):
    """ViewSet for UserInteraction model"""
    serializer_class = CreateInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInteraction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        interaction = serializer.save(user=self.request.user)

        # Track interaction event
        track_event(self.request.user.id, f'content_{interaction.interaction_type}', {
            'object_type': interaction.object_type,
            'object_id': interaction.object_id,
        })
