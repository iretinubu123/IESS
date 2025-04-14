from django.urls import path, include, re_path
from .views import  logout_view
from rest_framework_simplejwt.views import TokenRefreshView
from .views import StudentTrackingView 
from .views import StudentPerformanceView  
from .views import StudentPerformanceDetailView 
from .views import CareerPredictionView 
from .views import AcademicAdvisingView
from .import views
urlpatterns = [
   path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('student-tracking/', StudentTrackingView.as_view(), name='student-tracking'),
    path('student-performance/', StudentPerformanceView.as_view(), name='student-performance'),
    path('student-performance/<int:pk>/', StudentPerformanceDetailView.as_view(), name='student-performance-detail'),
    path("career/predict-career/", CareerPredictionView.as_view(), name="predict-career"),
    path("academic-advising/", AcademicAdvisingView.as_view(), name="academic_advising"),
     path('sentiment/', include('api.sentiment_analysis.urls')),
       path('gamification/', include('api.gamification.urls')),
]

