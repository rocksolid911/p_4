"""
Views for recommendations
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import RecommendationService
from .serializers import RecommendationSerializer
from analytics.mixpanel_client import track_event


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    """
    Get personalized recommendations for the authenticated user

    GET /api/recommendations/?limit=20
    """
    limit = int(request.query_params.get('limit', 20))
    limit = min(limit, 100)  # Cap at 100

    service = RecommendationService()
    recommendations = service.get_recommendations_for_user(request.user.id, limit)

    # Track event
    track_event(request.user.id, 'content_recommended', {
        'count': len(recommendations),
        'limit': limit,
    })

    serializer = RecommendationSerializer(recommendations, many=True)
    return Response(serializer.data)
