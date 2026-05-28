from django.db import models
from django.conf import settings


class Submission(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name='submissions')
    exam = models.ForeignKey('exams.Exam', on_delete=models.SET_NULL, null=True, blank=True, related_name='submissions')
    submitted_sql = models.TextField()
    submission_time = models.DateTimeField(auto_now_add=True)
    execution_status = models.CharField(max_length=50, blank=True, default='')
    score = models.IntegerField(default=0)

    class Meta:
        db_table = 'submission'
