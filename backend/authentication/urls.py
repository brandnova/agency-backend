from django.urls import path
from .views import (
    UserRegistrationView, VerifyEmailView, UserLoginView, ProtectedView,
    ForgotPasswordView, ResetPasswordView, UserProfileView, ChangePasswordView,
    LogoutView, LogoutAllView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout-all'),
]