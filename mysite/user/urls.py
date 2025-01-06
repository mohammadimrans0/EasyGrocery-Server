from django.urls import path
from .views import (
    UserRegistrationApiView,
    UserLoginApiView,
    UserLogoutApiView,
    ResetPasswordView,
    activate,
)

urlpatterns = [
    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutApiView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('activate/<str:uid64>/<str:token>/', activate, name='activate'),
]
