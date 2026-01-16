from django.db import models
from django.contrib.auth.models import User

class Chapter(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    LANGUAGE_CHOICES = (
        ('hi', 'Hindi'),
        ('en', 'English'),
    )

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    question = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    CORRECT_CHOICES = (
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    )
    correct_option = models.CharField(max_length=1, choices=CORRECT_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]


class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total_questions}"