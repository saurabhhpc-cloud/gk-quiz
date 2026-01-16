from rest_framework import serializers
from .models import Chapter, Question
from .models import QuizScore
from django.contrib.auth.models import User


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'question',
            'option_a',
            'option_b',
            'option_c',
            'option_d'
        ]
class AnswerSubmitSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option = serializers.ChoiceField(
        choices=['A', 'B', 'C', 'D']
    )

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )


class QuizScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizScore
        fields = ['score', 'total_questions', 'created_at']    