import torch
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .model_utils import predict_career

@api_view(["POST"])
def career_prediction_api(request):
    try:
        # Parse student data from request
        student_data = json.loads(request.body)

        # Validate required fields
        required_fields = [
            "Gender", "Favorite_Subjects", "Skills", "Extracurricular_Activities",
            "Personality_Traits", "Preferred_Work_Style"
        ]
        missing_fields = [field for field in required_fields if field not in student_data]
        if missing_fields:
            return JsonResponse({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

        # Get career prediction
        predicted_career = predict_career(student_data)

        return JsonResponse({"predicted_career": predicted_career})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
