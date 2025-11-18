"""
URL patterns for Bills
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BillViewSet, UserInteractionViewSet

router = DefaultRouter()
router.register(r'', BillViewSet, basename='bill')
router.register(r'interactions', UserInteractionViewSet, basename='interaction')

urlpatterns = router.urls
