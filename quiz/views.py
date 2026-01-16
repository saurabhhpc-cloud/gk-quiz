from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chapter, Question
from .serializers import ChapterSerializer, QuestionSerializer
import random
from .serializers import AnswerSubmitSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, QuizScoreSerializer
from .models import QuizScore

# 1️⃣ Chapter List API
class ChapterListAPI(APIView):
    def get(self, request):
        chapters = Chapter.objects.filter(is_active=True)
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 2️⃣ Chapterwise Questions API
class ChapterQuestionsAPI(APIView):
    def get(self, request, chapter_id):
        language = request.GET.get('lang', 'en')
        questions = Question.objects.filter(
            chapter_id=chapter_id,
            language=language
        )
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 3️⃣ Random Quiz API
class RandomQuizAPI(APIView):
    def get(self, request):
        print("TOTAL QUESTIONS:", Question.objects.count())

        language = request.GET.get('lang', 'en')
        limit = int(request.GET.get('limit', 10))

        qs = Question.objects.filter(language=language)
        print("FILTERED QUESTIONS:", qs.count())

        serializer = QuestionSerializer(qs[:limit], many=True)
        return Response(serializer.data)


class SubmitAnswerAPI(APIView):
    def post(self, request):
        serializer = AnswerSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        question_id = serializer.validated_data['question_id']
        selected_option = serializer.validated_data['selected_option']

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response(
                {"error": "Question not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        is_correct = question.correct_option == selected_option

        return Response(
            {
                "question_id": question_id,
                "is_correct": is_correct
            },
            status=status.HTTP_200_OK
        )
class SubmitQuizAPI(APIView):
    def post(self, request):
        """
        Expected payload:
        {
          "answers": [
            {"question_id": 1, "selected_option": "A"},
            {"question_id": 2, "selected_option": "C"}
          ]
        }
        """

        answers = request.data.get("answers", [])

        if not answers:
            return Response(
                {"error": "No answers submitted"},
                status=status.HTTP_400_BAD_REQUEST
            )

        score = 0
        total = len(answers)
        result = []

        for item in answers:
            qid = item.get("question_id")
            selected = item.get("selected_option")

            try:
                question = Question.objects.get(id=qid)
                correct = question.correct_option == selected
            except Question.DoesNotExist:
                correct = False

            if correct:
                score += 1

            result.append({
                "question_id": qid,
                "is_correct": correct
            })

        return Response(
            {
                "total_questions": total,
                "correct_answers": score,
                "score": score,
                "result": result
            },
            status=status.HTTP_200_OK
        )
class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered successfully"})
    
class LoginAPI(APIView):
    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })  
     
class SaveScoreAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        score = request.data.get('score')
        total = request.data.get('total_questions')

        QuizScore.objects.create(
            user=request.user,
            score=score,
            total_questions=total
        )

        return Response({"message": "Score saved"})
        
class ScoreHistoryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        scores = QuizScore.objects.filter(user=request.user)
        serializer = QuizScoreSerializer(scores, many=True)
        return Response(serializer.data)