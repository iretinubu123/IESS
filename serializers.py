from rest_framework import serializers
from .models import StudentPerformance
from .models import StudentCareerProfile
from django.contrib.auth.models import User

class StudentPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPerformance
        fields = '__all__'

class StudentCareerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCareerProfile
        fields = "__all__"
    
    class UserSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user