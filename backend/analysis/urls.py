"""
URL patterns for analysis app
"""
from django.urls import path
from .views import summarize_bill, analyze_news

urlpatterns = [
    path('bills/summarize/', summarize_bill, name='summarize-bill'),
    path('news/analyze/', analyze_news, name='analyze-news'),
]
