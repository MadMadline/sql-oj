from rest_framework import serializers
from .models import Exam, ExamQuestion


class ExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamQuestion
        fields = ('id', 'question', 'score')


class ExamSerializer(serializers.ModelSerializer):
    exam_questions = ExamQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ('teacher', 'created_at')
