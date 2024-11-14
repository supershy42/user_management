from django.urls import path, include
from user_management.views import UserRegistrationView, EmailVerificationView, UserLoginView

urlpatterns = [
    path('user/', include('user_management.urls')),
]
