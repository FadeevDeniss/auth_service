from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):

    username = models.CharField(null=True, blank=True)
    email = models.EmailField(db_index=True, unique=True)

    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
