from django.db import models
from django.conf import settings


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    description = models.TextField()
    title = models.CharField(max_length=255, blank=True, default='')
    sample_input = models.TextField(blank=True, null=True)
    sample_output = models.TextField(blank=True, null=True)
    create_table_sql = models.TextField(blank=True, null=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name='questions'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'question'
        ordering = ['-created_at']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    correct_sql = models.TextField()

    class Meta:
        db_table = 'answer'


class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='test_cases')
    test_input = models.TextField(blank=True, null=True)
    expected_output = models.TextField()

    class Meta:
        db_table = 'test_case'
