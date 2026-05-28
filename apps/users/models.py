from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    PERMISSION_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    permission_level = models.CharField(
        max_length=10, choices=PERMISSION_CHOICES,
        null=True, blank=True
    )
    teacher = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='students',
        limit_choices_to={'user_type': 'teacher'}
    )

    class Meta:
        db_table = 'user'
