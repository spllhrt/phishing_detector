# app/urls.py
from django.urls import path
from .views import RegisterView, LoginView, PhishingDetectionView

urlpatterns = [
    path('detect/', PhishingDetectionView.as_view(), name='detect_phishing'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]

