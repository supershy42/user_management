from django.urls import path, include

urlpatterns = [
    path('api/user/', include('user_management.urls')),
    path('api/friend/', include('friend.urls')),
]
