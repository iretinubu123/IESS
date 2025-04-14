from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SentimentAnalysisSerializer
from .services import analyze_sentiment
from rest_framework.permissions import AllowAny

class SentimentAnalysisView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SentimentAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data["text"]
            sentiment_result = analyze_sentiment(text)
            return Response(sentiment_result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
