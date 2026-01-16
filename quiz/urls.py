from django.urls import path
from .views import (
    ChapterListAPI,
    ChapterQuestionsAPI,
    RandomQuizAPI,
    RegisterAPI,
    LoginAPI,
    SubmitQuizAPI,
    SaveScoreAPI,
    ScoreHistoryAPI,
)

urlpatterns = [
    path('chapters/', ChapterListAPI.as_view()),
    path('chapters/<int:chapter_id>/questions/', ChapterQuestionsAPI.as_view()),
    path('random-quiz/', RandomQuizAPI.as_view()),

    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('submit-quiz/', SubmitQuizAPI.as_view()),
    path('save-score/', SaveScoreAPI.as_view()),
    path('score-history/', ScoreHistoryAPI.as_view()),
]
