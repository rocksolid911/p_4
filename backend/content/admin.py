"""
Admin configuration for content app
"""
from django.contrib import admin
from .models import Bill, BillSummary, NewsArticle, NewsAnalysis, UserInteraction


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['title', 'parliament_house', 'status', 'introduced_on', 'created_at']
    list_filter = ['status', 'parliament_house', 'state']
    search_fields = ['title', 'full_text']
    date_hierarchy = 'introduced_on'


@admin.register(BillSummary)
class BillSummaryAdmin(admin.ModelAdmin):
    list_display = ['bill', 'language_code', 'created_by', 'created_at']
    list_filter = ['language_code']
    search_fields = ['bill__title', 'summary_short']


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'source_name', 'published_at', 'language_code', 'created_at']
    list_filter = ['source_name', 'language_code']
    search_fields = ['title', 'content']
    date_hierarchy = 'published_at'


@admin.register(NewsAnalysis)
class NewsAnalysisAdmin(admin.ModelAdmin):
    list_display = ['article', 'sentiment', 'leaning', 'propaganda_score', 'created_at']
    list_filter = ['sentiment', 'leaning', 'emotional_language_detected']
    search_fields = ['article__title', 'explanation']


@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ['user', 'object_type', 'object_id', 'interaction_type', 'created_at']
    list_filter = ['object_type', 'interaction_type']
    search_fields = ['user__email']
    date_hierarchy = 'created_at'
