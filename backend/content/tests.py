"""
Tests for content app
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Bill, BillSummary, NewsArticle, NewsAnalysis, UserInteraction

User = get_user_model()


class BillModelTest(TestCase):
    """Test Bill model"""

    def setUp(self):
        self.bill = Bill.objects.create(
            title='Test Bill',
            full_text='This is a test bill content',
            parliament_house='lok_sabha',
            status='introduced',
            topics=['Economy', 'Finance']
        )

    def test_bill_creation(self):
        """Test bill creation"""
        self.assertEqual(self.bill.title, 'Test Bill')
        self.assertEqual(self.bill.parliament_house, 'lok_sabha')
        self.assertEqual(len(self.bill.topics), 2)

    def test_bill_str(self):
        """Test bill string representation"""
        self.assertEqual(str(self.bill), 'Test Bill')


class BillSummaryModelTest(TestCase):
    """Test BillSummary model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )
        self.bill = Bill.objects.create(
            title='Test Bill',
            full_text='This is a test bill',
            parliament_house='lok_sabha'
        )
        self.summary = BillSummary.objects.create(
            bill=self.bill,
            language_code='en',
            summary_short='Short summary',
            summary_detailed='Detailed summary',
            pros=['Pro 1', 'Pro 2'],
            cons=['Con 1', 'Con 2'],
            created_by=self.user
        )

    def test_summary_creation(self):
        """Test summary creation"""
        self.assertEqual(self.summary.bill, self.bill)
        self.assertEqual(self.summary.language_code, 'en')
        self.assertEqual(len(self.summary.pros), 2)


class NewsArticleModelTest(TestCase):
    """Test NewsArticle model"""

    def setUp(self):
        self.article = NewsArticle.objects.create(
            title='Test Article',
            content='Test article content',
            source_url='https://example.com/article',
            source_name='Test News',
            topics=['Politics']
        )

    def test_article_creation(self):
        """Test article creation"""
        self.assertEqual(self.article.title, 'Test Article')
        self.assertEqual(self.article.source_name, 'Test News')
