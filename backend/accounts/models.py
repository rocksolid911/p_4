"""
User and Profile models for LokSathi
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model with email as unique identifier"""

    ROLE_CHOICES = [
        ('citizen', 'Citizen'),
        ('researcher', 'Researcher'),
        ('admin', 'Admin'),
    ]

    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255)

    # Profile fields
    state = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    preferred_languages = models.JSONField(default=list)  # ['en', 'hi', 'mr']
    interests = models.JSONField(default=list)  # ['Economy', 'Education', etc.]

    # Role and permissions
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')

    # Status fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    @property
    def is_researcher(self):
        return self.role in ['researcher', 'admin']

    @property
    def is_admin(self):
        return self.role == 'admin'
