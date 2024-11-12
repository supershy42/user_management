from django.urls import path
from user_management.views import UserRegistrationView, EmailVerificationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify-email'),
]
