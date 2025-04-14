import os
import json
import joblib
import pandas as pd
from pgmpy.inference import VariableElimination

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

from .models import StudentPerformance, StudentCareerProfile
from .serializers import StudentPerformanceSerializer, StudentCareerProfileSerializer
from .career_prediction.predictor import predict_career
from .academic_advising.bayesian_advisor import recommend_course

# ======================
# Paths for Bayesian Model
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "academic_advising", "bayesian_model.joblib")
ENCODER_PATH = os.path.join(BASE_DIR, "academic_advising", "bayesian_encoders.joblib")

# ======================
# Load Bayesian Model & Encoders
# ======================
if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = joblib.load(f)
    with open(ENCODER_PATH, "rb") as f:
        encoders = joblib.load(f)
    inference = VariableElimination(model)
else:
    model, encoders, inference = None, None, None


# ======================
# Auth Utilities
# ======================
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# ======================
# Authentication Views
# ======================
@csrf_exempt
@require_POST
def signup(request):
    data = json.loads(request.body)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return JsonResponse({'error': 'All fields are required'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email already exists'}, status=400)

    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)

        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'name': user.username,
                'email': user.email
            },
            'token': token.key
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def login(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return JsonResponse({'error': 'Username and password are required'}, status=400)

    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'name': user.username,
                'email': user.email
            },
            'token': token.key
        })
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=400)

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"message": "Successfully logged out"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


# ======================
# Student Performance Views
# ======================
class StudentTrackingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_name = request.user.username
        student_data = StudentPerformance.objects.filter(student=request.user)
        serializer = StudentPerformanceSerializer(student_data, many=True)

        return Response({
            'username': user_name,
            'performance_data': serializer.data
        })


class StudentPerformanceView(generics.ListCreateAPIView):
    serializer_class = StudentPerformanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Check if Swagger is generating schema (used in drf-yasg)
        if getattr(self, 'swagger_fake_view', False):
            return StudentPerformance.objects.none()

        # Ensure the user is authenticated
        if self.request.user.is_authenticated:
            return StudentPerformance.objects.filter(student=self.request.user)

        return StudentPerformance.objects.none()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class StudentPerformanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentPerformanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Check if Swagger is generating schema (used in drf-yasg)
        if getattr(self, 'swagger_fake_view', False):
            return StudentPerformance.objects.none()

        # Ensure the user is authenticated
        if self.request.user.is_authenticated:
            return StudentPerformance.objects.filter(student=self.request.user)

        return StudentPerformance.objects.none()


# ======================
# Career Prediction Views
# ======================
class CareerPredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        interests = data.get("interests", [])
        skills = data.get("skills", [])
        grades = data.get("grades", {})

        predicted_career = predict_career(interests, skills, grades)

        StudentCareerProfile.objects.create(
            student=request.user,
            interests=interests,
            skills=skills,
            grades=grades,
            predicted_career=predicted_career
        )

        return Response({"predicted_career": predicted_career}, status=status.HTTP_200_OK)


class StudentCareerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = StudentCareerProfile.objects.filter(student=request.user)
        serializer = StudentCareerProfileSerializer(profiles, many=True)
        return Response(serializer.data)


# ======================
# Academic Advising View (Bayesian)
# ======================
class AcademicAdvisingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not model or not encoders:
            return Response({"error": "Model not found. Train the Bayesian advisor first."}, status=500)

        try:
            data = request.data
            gpa = float(data["GPA"])
            study_hours = int(data["Study_Hours"])
            preferred_subject = data["Preferred_Subject"].strip().capitalize()
            learning_style = data["Learning_Style"].strip().capitalize()
            career_aspiration = data["Career_Aspiration"].strip().capitalize()
            interest_area = data["Interest_Area"].strip().capitalize()

            encoded_data = {
                "GPA": gpa,
                "Study_Hours": study_hours,
                "Preferred_Subject": encoders["Preferred_Subject"].transform([preferred_subject])[0],
                "Learning_Style": encoders["Learning_Style"].transform([learning_style])[0],
                "Career_Aspiration": encoders["Career_Aspiration"].transform([career_aspiration])[0],
                "Interest_Area": encoders["Interest_Area"].transform([interest_area])[0]
            }

            query_result = inference.map_query(variables=["Recommended_Course"], evidence=encoded_data)
            recommended_course = encoders["Recommended_Course"].inverse_transform([query_result["Recommended_Course"]])[0]

            return Response({"recommended_course": recommended_course})
        except KeyError as e:
            return Response({"error": f"Invalid input key: {str(e)}"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
