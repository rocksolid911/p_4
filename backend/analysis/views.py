"""
Views for AI analysis endpoints
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from content.models import Bill, BillSummary, NewsArticle, NewsAnalysis
from content.serializers import BillSummarySerializer, NewsAnalysisSerializer
from .services.bill_summarizer import BillSummarizerService
from .services.news_analyzer import NewsBiasAnalyzerService
from analytics.mixpanel_client import track_event


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def summarize_bill(request):
    """
    Summarize a bill in multiple languages

    POST /api/analysis/bills/summarize/
    {
        "bill_id": 123,  // OR "text": "full bill text"
        "languages": ["en", "hi", "mr"]
    }
    """
    bill_id = request.data.get('bill_id')
    bill_text = request.data.get('text')
    languages = request.data.get('languages', ['en'])

    # Get bill text
    if bill_id:
        try:
            bill = Bill.objects.get(id=bill_id)
            bill_text = bill.full_text
        except Bill.DoesNotExist:
            return Response(
                {'error': 'Bill not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    elif not bill_text:
        return Response(
            {'error': 'Either bill_id or text is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        bill = None

    # Generate summaries
    summarizer = BillSummarizerService()
    summaries_data = summarizer.process(bill_text, languages)

    # Save summaries if bill exists
    saved_summaries = []
    if bill:
        for lang_code, summary_data in summaries_data.items():
            summary, created = BillSummary.objects.update_or_create(
                bill=bill,
                language_code=lang_code,
                defaults={
                    'summary_short': summary_data['summary_short'],
                    'summary_detailed': summary_data['summary_detailed'],
                    'key_points': summary_data['key_points'],
                    'pros': summary_data['pros'],
                    'cons': summary_data['cons'],
                    'created_by': request.user,
                }
            )
            saved_summaries.append(summary)

        # Track event
        track_event(request.user.id, 'bill_summarized', {
            'bill_id': bill.id,
            'languages': languages,
        })

        return Response(BillSummarySerializer(saved_summaries, many=True).data)
    else:
        # Return raw summaries without saving
        return Response(summaries_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_news(request):
    """
    Analyze a news article for bias and sentiment

    POST /api/analysis/news/analyze/
    {
        "article_id": 123,  // OR "text": "article content"
        "language": "en"
    }
    """
    article_id = request.data.get('article_id')
    article_text = request.data.get('text')
    language = request.data.get('language', 'en')

    # Get article text
    if article_id:
        try:
            article = NewsArticle.objects.get(id=article_id)
            article_text = article.content
        except NewsArticle.DoesNotExist:
            return Response(
                {'error': 'Article not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    elif not article_text:
        return Response(
            {'error': 'Either article_id or text is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        article = None

    # Analyze article
    analyzer = NewsBiasAnalyzerService()
    analysis_data = analyzer.process(article_text, language)

    # Save analysis if article exists
    if article:
        analysis = NewsAnalysis.objects.create(
            article=article,
            sentiment=analysis_data['sentiment'],
            leaning=analysis_data['leaning'],
            propaganda_score=analysis_data['propaganda_score'],
            explanation=analysis_data['explanation'],
            emotional_language_detected=analysis_data['emotional_language_detected'],
            emotional_phrases=analysis_data['emotional_phrases'],
            language_code=language,
        )

        # Track event
        track_event(request.user.id, 'news_article_analyzed', {
            'article_id': article.id,
            'sentiment': analysis_data['sentiment'],
            'leaning': analysis_data['leaning'],
        })

        return Response(NewsAnalysisSerializer(analysis).data)
    else:
        # Return raw analysis without saving
        return Response(analysis_data)
