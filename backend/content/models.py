"""
Models for Bills, News, and user interactions
"""
from django.db import models
from django.conf import settings


class Bill(models.Model):
    """Model for legislative bills"""

    HOUSE_CHOICES = [
        ('lok_sabha', 'Lok Sabha'),
        ('rajya_sabha', 'Rajya Sabha'),
        ('state_assembly', 'State Assembly'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('introduced', 'Introduced'),
        ('in_committee', 'In Committee'),
        ('passed_lower', 'Passed Lower House'),
        ('passed_upper', 'Passed Upper House'),
        ('enacted', 'Enacted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    title = models.CharField(max_length=500)
    full_text = models.TextField()
    source_url = models.URLField(blank=True)
    parliament_house = models.CharField(max_length=50, choices=HOUSE_CHOICES)
    introduced_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='introduced')

    # Metadata
    state = models.CharField(max_length=100, blank=True)  # For state bills
    topics = models.JSONField(default=list)  # ['Economy', 'Education', etc.]

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bills'
        ordering = ['-introduced_on', '-created_at']
        indexes = [
            models.Index(fields=['status', 'parliament_house']),
            models.Index(fields=['introduced_on']),
        ]

    def __str__(self):
        return self.title


class BillSummary(models.Model):
    """Model for bill summaries in multiple languages"""

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='summaries')
    language_code = models.CharField(max_length=10)  # 'en', 'hi', 'mr', etc.

    summary_short = models.TextField()  # 2-3 sentences
    summary_detailed = models.TextField()  # Detailed explanation
    pros = models.JSONField(default=list)  # List of pros
    cons = models.JSONField(default=list)  # List of cons
    key_points = models.JSONField(default=list)  # List of key points

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_summaries'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bill_summaries'
        ordering = ['-created_at']
        unique_together = ['bill', 'language_code']
        indexes = [
            models.Index(fields=['bill', 'language_code']),
        ]

    def __str__(self):
        return f"{self.bill.title} - {self.language_code}"


class NewsArticle(models.Model):
    """Model for news articles"""

    title = models.CharField(max_length=500)
    content = models.TextField()
    source_url = models.URLField(unique=True)
    source_name = models.CharField(max_length=200)

    published_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    topics = models.JSONField(default=list)
    language_code = models.CharField(max_length=10, default='en')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'news_articles'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['published_at']),
            models.Index(fields=['source_name']),
        ]

    def __str__(self):
        return self.title


class NewsAnalysis(models.Model):
    """Model for news bias and sentiment analysis"""

    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]

    LEANING_CHOICES = [
        ('neutral', 'Neutral'),
        ('govt_leaning', 'Government Leaning'),
        ('opposition_leaning', 'Opposition Leaning'),
        ('unclear', 'Unclear'),
    ]

    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='analyses')

    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES)
    leaning = models.CharField(max_length=30, choices=LEANING_CHOICES)
    propaganda_score = models.FloatField(default=0.0)  # 0.0 to 1.0
    explanation = models.TextField()  # Why classified this way

    # Detailed analysis
    emotional_language_detected = models.BooleanField(default=False)
    emotional_phrases = models.JSONField(default=list)

    language_code = models.CharField(max_length=10, default='en')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'news_analyses'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['article', 'language_code']),
        ]

    def __str__(self):
        return f"{self.article.title} - {self.sentiment}"


class UserInteraction(models.Model):
    """Model for tracking user interactions with content"""

    OBJECT_TYPE_CHOICES = [
        ('bill', 'Bill'),
        ('news', 'News Article'),
    ]

    INTERACTION_TYPE_CHOICES = [
        ('view', 'View'),
        ('like', 'Like'),
        ('save', 'Save'),
        ('share', 'Share'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interactions')
    object_type = models.CharField(max_length=20, choices=OBJECT_TYPE_CHOICES)
    object_id = models.IntegerField()
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_interactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'object_type', 'object_id']),
            models.Index(fields=['user', 'interaction_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.interaction_type} - {self.object_type}:{self.object_id}"
