from django.urls import path, include
from user_management.views import UserRegistrationView, EmailVerificationView, UserLoginView

urlpatterns = [
    path('api/user/', include('user_management.urls')),
]
