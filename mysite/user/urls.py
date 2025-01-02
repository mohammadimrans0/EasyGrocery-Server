from django.urls import path
from .views import (
    UserRegistrationApiView,
    UserLoginApiView,
    UserLogoutApiView,
    activate,
)

urlpatterns = [
    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutApiView.as_view(), name='logout'),
    path('activate/<str:uid64>/<str:token>/', activate, name='activate'),
]
