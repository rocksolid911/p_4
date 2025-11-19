"""
Tests for accounts app
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User


class UserModelTest(TestCase):
    """Test User model"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.name, 'Test User')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_str(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'test@example.com')


class UserRegistrationTest(APITestCase):
    """Test user registration endpoint"""

    def test_user_registration(self):
        """Test successful user registration"""
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'name': 'New User',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'state': 'Maharashtra',
            'preferred_languages': ['en', 'hi'],
            'interests': ['Economy', 'Education']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('user', response.data)

    def test_user_registration_password_mismatch(self):
        """Test registration with password mismatch"""
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'name': 'New User',
            'password': 'newpass123',
            'password_confirm': 'differentpass',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTest(APITestCase):
    """Test user login endpoint"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_user_login(self):
        """Test successful login"""
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
