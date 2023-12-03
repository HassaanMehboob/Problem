from django.urls import path
from .views import RegisterUserView, UserLoginView, PasswordResetView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('password/reset/', PasswordResetView.as_view(), name='user_password_reset'),
]
