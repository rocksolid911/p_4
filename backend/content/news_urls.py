"""
URL patterns for News
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsArticleViewSet

router = DefaultRouter()
router.register(r'', NewsArticleViewSet, basename='news')

urlpatterns = router.urls
