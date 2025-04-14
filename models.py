from django.db import models
from django.contrib.auth.models import User
from transformers import pipeline
from django.utils import timezone

class StudentPerformance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="performance")
    subject = models.CharField(max_length=100)
    grade = models.FloatField()  # Grade stored as a float
    gpa = models.FloatField(blank=True, null=True)  # Calculated GPA
    semester = models.CharField(max_length=20, default="Fall 2025")  # e.g., "Fall 2025"
    date_recorded = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date_recorded"]

    def __str__(self):
        return f"{self.student.username} - {self.subject}: {self.grade}"


class StudentCareerProfile(models.Model):
    student_id = models.IntegerField()
    career_prediction = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Student {self.student_id}: {self.career_prediction}"
 
 